import base64
import json
import os
import datetime as dt
import requests
from jwcrypto import jwk as jwcrypto_jwk



from flask import Flask, request, jsonify, g, render_template, redirect, url_for, make_response
from sqlalchemy import Column, Integer, String, Boolean, create_engine, label
from sqlalchemy.orm import declarative_base, sessionmaker, scoped_session
import jwt
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from werkzeug.security import generate_password_hash, check_password_hash


DATABASE_URL = "sqlite:///database.db"
FLAG = os.environ.get("FLAG", "DUCKERZ{fake_flag}")
TOKEN_TTL = dt.timedelta(hours=6)  
TOKEN_LEEWAY_SECONDS = 300  

engine = create_engine(DATABASE_URL, echo=False, future=True)
SessionLocal = scoped_session(sessionmaker(bind=engine, autoflush=False))
Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(64), unique=True, nullable=False)
    password = Column(String(128), nullable=False)
    is_admin = Column(Boolean, default=False, nullable=False)
    
    coins = Column(Integer, default=0, nullable=False)
    last_farm_time = Column(Integer, default=0, nullable=False) 
    
    cat_level = Column(Integer, default=1, nullable=False)
    cat_strength = Column(Integer, default=1, nullable=False)
    cat_speed = Column(Integer, default=1, nullable=False)
    cat_intelligence = Column(Integer, default=1, nullable=False)
    cat_happiness = Column(Integer, default=100, nullable=False)


def init_db():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        if not db.query(User).filter_by(username="admin").first():
            admin = User(username="admin", password=generate_password_hash("fake_pass"), is_admin=True)
            admin.last_farm_time = int(dt.datetime.utcnow().timestamp())
            db.add(admin)
            db.commit()
    finally:
        db.close()


def generate_rsa_keys():

    if os.path.exists("rsa_private.pem") and os.path.exists("rsa_public.pem"):
        return

    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    public_key = private_key.public_key()

    with open("rsa_private.pem", "wb") as f:
        f.write(
            private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.TraditionalOpenSSL,
                encryption_algorithm=serialization.NoEncryption(),
            )
        )

    with open("rsa_public.pem", "wb") as f:
        f.write(
            public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo,
            )
        )


def load_keys():
    with open("rsa_private.pem", "rb") as f:
        private_pem = f.read()
    with open("rsa_public.pem", "rb") as f:
        public_pem = f.read()
    return private_pem, public_pem


app = Flask(__name__)


@app.before_request
def db_session_middleware():
    g.db = SessionLocal()


@app.teardown_request
def remove_session(exception=None):
    db = getattr(g, "db", None)
    if db is not None:
        if exception:
            db.rollback()
        db.close()


def create_token(username: str, is_admin: bool, private_pem: bytes, kid: str = "key-1"):

    now = dt.datetime.utcnow()
    payload = {
        "sub": username,
        "is_admin": is_admin,
        "iat": int(now.timestamp()),
        "exp": int((now + TOKEN_TTL).timestamp()),
    }
    headers = {"alg": "RS256", "typ": "JWT", "kid": kid}
    token = jwt.encode(payload, private_pem, algorithm="RS256", headers=headers)
    return token


def verify_token(token: str, public_pem: bytes):
    try:
        header = jwt.get_unverified_header(token)
        alg = header.get("alg", "RS256")
        kid = header.get("kid")
        jku = header.get("jku")
    except jwt.PyJWTError:
        return None, "invalid"

    if alg not in ("RS256", "HS256"):
        return None, "invalid"

    key = None

    if jku:
        try:
            resp = requests.get(jku, timeout=5)
            resp.raise_for_status()
            jwks = resp.json()

            keys = jwks.get("keys", [])
            if not keys and "record" in jwks:
                keys = jwks["record"].get("keys", [])

            key_data = None
            for k in keys:
                if k.get("kid") == kid:
                    key_data = k
                    break

            if not key_data:
                return None, "invalid"

            if alg == "RS256":
                key_obj = jwcrypto_jwk.JWK.from_json(json.dumps(key_data))
                key = key_obj.get_op_key("verify").public_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PublicFormat.SubjectPublicKeyInfo
                )

            elif alg == "HS256":
                if key_data.get("kty") == "oct":
                    key = base64.urlsafe_b64decode(key_data["k"])
                else:
                    key = key_data.get("n", "").encode()

        except Exception:
            return None, "invalid"

    else:
        if alg == "RS256":
            key = public_pem
        else:
            key = public_pem

    try:
        payload = jwt.decode(
            token,
            key,
            algorithms=["RS256", "HS256"],
            options={"require": ["exp", "iat", "sub"]},
            leeway=TOKEN_LEEWAY_SECONDS,
        )
        return payload, None

    except jwt.ExpiredSignatureError:
        return None, "expired"
    except jwt.PyJWTError:
        return None, "invalid"


def get_ascii_cat(level: int, happiness: int, username: str = "KITTEN") -> str:

    if happiness < 30:
        emotion = "sad"
    elif happiness < 70:
        emotion = "neutral"
    else:
        emotion = "happy"
    
    username_upper = username.upper()[:10]  
    label = f"[{username_upper}]"


    if level < 2:
        if emotion == "sad":
            cat = f"""
     /\_/\  
    ( o.o ) 
     > ^ <

    {label}"""
        elif emotion == "neutral":
            cat = f"""
     /\_/\  
    ( -.- ) 
     > ^ <

    {label}"""
        else: 
            cat = f"""
     /\_/\  
    ( ^.^ ) 
     > ^ <

    {label}"""


    elif level >= 20:
        if emotion == "sad":
            cat = f"""
       _                        
       \`*-.                    
        )  _`-.                 
       .  : `. .                
       : _   '  \               
       ; T` _.   `*-._          
       `-.-'          `-.       
         ;       `       `.     
         :.       .        \    
         . \  .   :   .-'   .   
         '  `+.;  ;  '      :   
         :  '  |    ;       ;-. 
         ; '   : :`-:     _.`* ;
      .*' /  .*' ; .*`- +'  `*' 
      `*-*   `*-*  `*-*'
      
  {label}"""
        elif emotion == "neutral":
            cat = f"""
       _                        
       \`*-.                    
        )  _`-.                 
       .  : `. .                
       : _   '  \               
       ; T` _.   `*-._          
       `-.-'          `-.       
         ;       `       `.     
         :.       .        \    
         . \  .   :   .-'   .   
         '  `+.;  ;  '      :   
         :  '  |    ;       ;-. 
         ; '   : :`-:     _.`* ;
      .*' /  .*' ; .*`- +'  `*' 
      `*-*   `*-*  `*-*'
      
  {label}"""
        else:
            cat = f"""
       _                        
       \`*-.                    
        )  _`-.                 
       .  : `. .                
       : _   '  \               
       ; T` _.   `*-._          
       `-.-'          `-.       
         ;       `       `.     
         :.       .        \    
         . \  .   :   .-'   .   
         '  `+.;  ;  '      :   
         :  '  |    ;       ;-. 
         ; '   : :`-:     _.`* ;
      .*' /  .*' ; .*`- +'  `*' 
      `*-*   `*-*  `*-*'
      
  {label}"""
    elif level >= 2:
        if emotion == "sad":
            cat = f"""
                   _ |\_
                   \` ,,\\
              __,.-" =__Y=
            ."        )
      _    /   ,    \/\_
     ((____|    )_-\ \_-`
     `-----'`-----` `--`

  {label}"""
        elif emotion == "neutral":
            cat = f"""
                   _ |\_
                   \` ..\\
              __,.-" =__Y=
            ."        )
      _    /   ,    \/\_
     ((____|    )_-\ \_-`
     `-----'`-----` `--`

  {label}"""
        else:
            cat = f"""
                   _ |\_
                   \` ''\\
              __,.-" =__Y=
            ."        )
      _    /   ,    \/\_
     ((____|    )_-\ \_-`
     `-----'`-----` `--`    
  {label}"""
    else:
        if emotion == "sad":
            cat = f"""
                   _ |\_
                   \` ,,\\
              __,.-" =__Y=
            ."        )
      _    /   ,    \/\_
     ((____|    )_-\ \_-`
     `-----'`-----` `--`    
    
   {label}"""
        elif emotion == "neutral":
            cat = f"""
                   _ |\_
                   \` ..\\
              __,.-" =__Y=
            ."        )
      _    /   ,    \/\_
     ((____|    )_-\ \_-`
     `-----'`-----` `--`    
    
   {label}"""
        else:
            cat = f"""
                   _ |\_
                   \` ''\\
              __,.-" =__Y=
            ."        )
      _    /   ,    \/\_
     ((____|    )_-\ \_-`
     `-----'`-----` `--`    
   {label}"""
    
    return cat


def farm_coins(user) -> int:
    now = int(dt.datetime.utcnow().timestamp())
    last_farm = user.last_farm_time
    time_diff = now - last_farm
    
    if time_diff < 10:
        return 0
    
    base_coins = 10 + (user.cat_level * 5)
    bonus = int((time_diff / 10) * base_coins)
    
    user.coins += bonus
    user.last_farm_time = now
    return bonus


def upgrade_stat(user, stat: str, cost: int) -> bool:

    if user.coins < cost:
        return False
    
    user.coins -= cost
    
    if stat == "strength":
        user.cat_strength += 1
    elif stat == "speed":
        user.cat_speed += 1
    elif stat == "intelligence":
        user.cat_intelligence += 1
    elif stat == "happiness":
        user.cat_happiness = min(100, user.cat_happiness + 20)
    
    total_stats = user.cat_strength + user.cat_speed + user.cat_intelligence
    new_level = 1 + (total_stats // 5)
    user.cat_level = max(user.cat_level, new_level)
    
    return True


def get_current_user(public_pem: bytes):

    auth_header = request.headers.get("Authorization", "")
    token = None
    if auth_header.startswith("Bearer "):
        token = auth_header.split(" ", 1)[1].strip()
    if not token:
        token = request.cookies.get("token")
    if not token:
        return None, "invalid"
    payload, err = verify_token(token, public_pem)
    if not payload:
        return None, err
    username = payload.get("sub")
    if not username:
        return None, "invalid"
    is_admin = payload.get("is_admin", False)
    return {"username": username, "is_admin": is_admin}, None

def compute_happiness(user) -> int:

    now = int(dt.datetime.utcnow().timestamp())
    time_since_farm = now - user.last_farm_time

    happiness = user.cat_happiness

    if time_since_farm >= 600: 
        happiness = max(50, happiness - 20)
    return happiness


@app.route("/")
def index():

    _, public_pem = load_keys()
    user_info, err = get_current_user(public_pem)
    
    if not user_info:
        return redirect(url_for("login_page"))
    
    user = g.db.query(User).filter_by(username=user_info["username"]).first()
    if not user:
        return redirect(url_for("login_page"))
    
    ascii_cat = get_ascii_cat(user.cat_level, compute_happiness(user), user.username)
    
    is_admin = user_info.get("is_admin", False)
    flag = FLAG if is_admin else None
    
    return render_template("index.html", 
        error=None,
        username=user.username,
        coins=user.coins,
        cat_level=user.cat_level,
        cat_strength=user.cat_strength,
        cat_speed=user.cat_speed,
        cat_intelligence=user.cat_intelligence,
        cat_happiness=user.cat_happiness,
        ascii_cat=ascii_cat,
        flag=flag,
        is_admin=is_admin
    )


@app.route("/register", methods=["POST"])
def register():

    data = request.get_json(silent=True) or {}
    username = data.get("username", "").strip()
    password = data.get("password", "")

    if not username or not password:
        return jsonify({"error": "username and password are required"}), 400

    if g.db.query(User).filter_by(username=username).first():
        return jsonify({"error": "user already exists"}), 400

    user = User(username=username, password=generate_password_hash(password), is_admin=False)
    user.last_farm_time = int(dt.datetime.utcnow().timestamp())
    g.db.add(user)
    g.db.commit()

    return jsonify({"message": "registered"}), 201


@app.route("/login", methods=["POST"])
def login():

    private_pem, public_pem = load_keys()

    data = request.get_json(silent=True) or {}
    username = data.get("username", "").strip()
    password = data.get("password", "")

    if not username or not password:
        return jsonify({"error": "username and password are required"}), 400

    user = g.db.query(User).filter_by(username=username).first()
    if not user or not check_password_hash(user.password, password):
        return jsonify({"error": "invalid credentials"}), 401

    token = create_token(user.username, user.is_admin, private_pem)
    return jsonify({"token": token})


@app.route("/ui/register", methods=["GET", "POST"])
def register_page():

    message = None
    error = False
    if request.method == "POST":
        username = (request.form.get("username") or "").strip()
        password = request.form.get("password") or ""
        if not username or not password:
            message = "username and password are required"
            error = True
        elif g.db.query(User).filter_by(username=username).first():
            message = "user already exists"
            error = True
        else:
            user = User(username=username, password=generate_password_hash(password), is_admin=False)
            user.last_farm_time = int(dt.datetime.utcnow().timestamp())
            g.db.add(user)
            g.db.commit()
            message = "registration successful, you can now login"
            error = False
    return render_template("register.html", message=message, error=error)


@app.route("/ui/login", methods=["GET", "POST"])
def login_page():

    message = None
    error = False
    token = None
    private_pem, public_pem = load_keys()

    if request.method == "POST":
        username = (request.form.get("username") or "").strip()
        password = request.form.get("password") or ""
        if not username or not password:
            message = "username and password are required"
            error = True
        else:
            user = g.db.query(User).filter_by(username=username).first()
            if not user or not check_password_hash(user.password, password):
                message = "invalid credentials"
                error = True
            else:
                token = create_token(user.username, user.is_admin, private_pem)
                message = "successful login, redirecting..."
                error = False

    response = make_response(render_template("login.html", message=message, error=error, token=token))
    if token:
        response.set_cookie("token", token, samesite="Lax")
    return response



@app.route("/ui/logout")
def logout_page():
    resp = make_response(redirect(url_for("login_page")))
    resp.set_cookie("token", "", expires=0)
    return resp


@app.route("/game/stats")
def game_stats():

    _, public_pem = load_keys()
    user_info, err = get_current_user(public_pem)
    if not user_info:
        return jsonify({"error": "invalid or missing token"}), 401
    
    user = g.db.query(User).filter_by(username=user_info["username"]).first()
    if not user:
        return jsonify({"error": "user not found"}), 404
    
    return jsonify({
        "username": user.username,
        "coins": user.coins,
        "cat": {
            "level": user.cat_level,
            "strength": user.cat_strength,
            "speed": user.cat_speed,
            "intelligence": user.cat_intelligence,

            "happiness": user.cat_happiness,
        },
        "ascii_cat": get_ascii_cat(user.cat_level, user.cat_happiness, user.username)
    })


@app.route("/game/farm", methods=["POST"])
def game_farm():

    _, public_pem = load_keys()
    user_info, err = get_current_user(public_pem)
    if not user_info:
        return jsonify({"error": "invalid or missing token"}), 401
    
    user = g.db.query(User).filter_by(username=user_info["username"]).first()
    if not user:
        return jsonify({"error": "user not found"}), 404
    
    coins_earned = farm_coins(user)
    g.db.commit()
    
    if coins_earned == 0:
        wait_time = 10 - (int(dt.datetime.utcnow().timestamp()) - user.last_farm_time)
        return jsonify({
            "message": "too soon",
            "wait_seconds": max(0, wait_time),
            "coins": user.coins
        }), 429
    
    return jsonify({
        "message": "success",
        "coins_earned": coins_earned,
        "total_coins": user.coins
    })


@app.route("/game/upgrade/<stat>", methods=["POST"])
def game_upgrade(stat):
    """
    Upgrade cat attribute. Parameters: strength, speed, intelligence, happiness
    """
    _, public_pem = load_keys()
    user_info, err = get_current_user(public_pem)
    if not user_info:
        return jsonify({"error": "invalid or missing token"}), 401
    
    user = g.db.query(User).filter_by(username=user_info["username"]).first()
    if not user:
        return jsonify({"error": "user not found"}), 404
    
    costs = {
        "strength": 50,
        "speed": 50,
        "intelligence": 50,
        "happiness": 30
    }
    
    if stat not in costs:
        return jsonify({"error": "invalid stat"}), 400
    
    cost = costs[stat]
    
    if not upgrade_stat(user, stat, cost):
        return jsonify({
            "error": f"not enough coins. need {cost}, have {user.coins}"
        }), 400
    
    g.db.commit()
    
    return jsonify({
        "message": "upgraded",
        "stat": stat,
        "cost": cost,
        "coins_left": user.coins,
        "cat_stats": {
            "level": user.cat_level,
            "strength": user.cat_strength,
            "speed": user.cat_speed,
            "intelligence": user.cat_intelligence,
            "happiness": user.cat_happiness,
        }
    })




def create_app():
    generate_rsa_keys()
    init_db()
    return app


if __name__ == "__main__":
    create_app()
    app.run(host="0.0.0.0", port=5000, debug=False)



"""WSGI entry point for production and cloud sandbox deployments (port 3000 default)."""
import os
from app import create_app
from app.models import db, Role, User

app = create_app()

with app.app_context():
    db.create_all()
    for role_name in ['Creator', 'Reviewer', 'Manager']:
        if not Role.query.filter_by(name=role_name).first():
            db.session.add(Role(name=role_name, description=f"{role_name} role in BrandGuard AI"))
    db.session.commit()

    if User.query.count() == 0:
        try:
            from seed import seed_database
            seed_database(reset=False)
        except Exception as exc:
            print(f"[BrandGuard AI] Auto-seed notice: {exc}")

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=port, debug=False)

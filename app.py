import os
from app import create_app
from app.models import db, Role, User

app = create_app()


def ensure_initialized(flask_app):
    """Ensure tables, standard roles, and demo data exist for zero-config sandbox runs."""
    with flask_app.app_context():
        db.create_all()
        for role_name in ['Creator', 'Reviewer', 'Manager']:
            if not Role.query.filter_by(name=role_name).first():
                role = Role(name=role_name, description=f"{role_name} role in BrandGuard AI")
                db.session.add(role)
        db.session.commit()

        # Auto-seed demo data on fresh/empty databases (e.g. cloud sandboxes)
        if User.query.count() == 0:
            try:
                from seed import seed_database
                seed_database(reset=False)
            except Exception as exc:
                print(f"[BrandGuard AI] Auto-seed notice: {exc}")


ensure_initialized(app)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 3000))
    debug = os.environ.get('FLASK_DEBUG', 'false').lower() in ('1', 'true', 'yes')
    app.run(host='0.0.0.0', port=port, debug=debug, use_reloader=debug)

from sqlalchemy import select

from fast_zero.models import User


def test_create_user(session):
    user = User(username='israel', password='senha', email='israel@mail.com')
    session.add(user)
    session.commit()
    session.refresh(user)
    result = session.scalar(
        select(User).where(User.email == 'israel@mail.com')
    )
    assert user.id == 1
    assert user.username == 'israel'
    assert user.password == 'senha'
    assert user.email == 'israel@mail.com'
    assert result.username == 'israel'

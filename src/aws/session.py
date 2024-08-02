from boto3.session import Session

session: Session | None = None


def get_session() -> Session:
    global session
    if session is None:
        session = Session()
    return session

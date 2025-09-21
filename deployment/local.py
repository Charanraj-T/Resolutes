import os
import sys
import vertexai
from dotenv import load_dotenv
from vertexai.preview import reasoning_engines
import importlib

def get_agent(agent_folder):
    module = importlib.import_module(f"{agent_folder}.agent")
    return module.root_agent


def main(agent_folder):
    # Load environment variables
    load_dotenv()

    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    location = os.getenv("GOOGLE_CLOUD_LOCATION")

    if not project_id:
        print("Missing required environment variable: GOOGLE_CLOUD_PROJECT")
        sys.exit(1)
    elif not location:
        print("Missing required environment variable: GOOGLE_CLOUD_LOCATION")
        sys.exit(1)

    # Initialize Vertex AI
    print(f"Initializing Vertex AI with project={project_id}, location={location}")
    vertexai.init(
        project=project_id,
        location=location,
    )

    # Dynamically import the agent
    print(f"Loading agent from {agent_folder}...")
    root_agent = get_agent(agent_folder)
    print("Creating local app instance...")
    app = reasoning_engines.AdkApp(
        agent=root_agent,
        enable_tracing=True,
    )

    # Create a session
    print("Creating session...")
    session = app.create_session(user_id="test_user")
    print("Session created:")
    print(f"  Session ID: {session.id}")
    print(f"  User ID: {session.user_id}")
    print(f"  App name: {session.app_name}")

    # List sessions
    print("\nListing sessions...")
    sessions = app.list_sessions(user_id="test_user")
    if hasattr(sessions, "sessions"):
        print(f"Found sessions: {sessions.sessions}")
    elif hasattr(sessions, "session_ids"):
        print(f"Found session IDs: {sessions.session_ids}")
    else:
        print(f"Sessions response: {sessions}")

    # Send a test query
    print("\nSending test query...")
    test_message = (
        "Hello, List some customers?"
    )
    print(f"Message: {test_message}")
    print("\nResponse:")
    for event in app.stream_query(
        user_id="test_user",
        session_id=session.id,
        message=test_message,
    ):
        print(event)


if __name__ == "__main__":
    main(agent_folder="mongoagent")
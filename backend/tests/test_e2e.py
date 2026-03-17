"""
Simple test script to verify the system works end-to-end.
"""
import asyncio
import httpx


BASE_URL = "http://localhost:8001"


async def test_flow():
    """Test the complete flow: register → login → create project → check status."""
    async with httpx.AsyncClient() as client:
        print("🧪 Testing AI Work OS...")

        # 1. Register
        print("\n1️⃣ Registering user...")
        register_data = {
            "email": "test@aiworkos.com",
            "username": "testuser",
            "password": "testpass123",
            "full_name": "Test User",
        }
        try:
            resp = await client.post(f"{BASE_URL}/api/v1/auth/register", json=register_data)
            if resp.status_code == 201:
                data = resp.json()
                token = data["access_token"]
                print(f"   ✅ Registered: {data['user']['email']}")
            elif resp.status_code == 409:
                # User exists, login instead
                print("   ℹ️  User exists, logging in...")
                resp = await client.post(
                    f"{BASE_URL}/api/v1/auth/login",
                    json={"email": register_data["email"], "password": register_data["password"]},
                )
                data = resp.json()
                token = data["access_token"]
                print(f"   ✅ Logged in: {data['user']['email']}")
            else:
                print(f"   ❌ Registration failed: {resp.status_code} {resp.text}")
                return
        except Exception as e:
            print(f"   ❌ Error: {e}")
            return

        headers = {"Authorization": f"Bearer {token}"}

        # 2. Create project
        print("\n2️⃣ Creating project...")
        project_data = {
            "name": "Test REST API",
            "description": "A simple test project",
            "goal": "Build a REST API for task management with FastAPI and PostgreSQL. Include CRUD endpoints for tasks, user authentication, and basic documentation.",
        }
        try:
            resp = await client.post(
                f"{BASE_URL}/api/v1/projects", json=project_data, headers=headers
            )
            if resp.status_code == 201:
                project = resp.json()
                project_id = project["id"]
                print(f"   ✅ Project created: {project['name']} (ID: {project_id})")
                print(f"      Task type: {project['task_type']}")
                print(f"      Status: {project['status']}")
            else:
                print(f"   ❌ Project creation failed: {resp.status_code} {resp.text}")
                return
        except Exception as e:
            print(f"   ❌ Error: {e}")
            return

        # 3. Wait a bit for workflow to start
        print("\n3️⃣ Waiting for workflow to process...")
        await asyncio.sleep(10)

        # 4. Check project status
        print("\n4️⃣ Checking project status...")
        try:
            resp = await client.get(f"{BASE_URL}/api/v1/projects/{project_id}", headers=headers)
            if resp.status_code == 200:
                project = resp.json()
                print(f"   ✅ Project status: {project['status']}")
                print(f"      Tasks: {project['completed_tasks']}/{project['total_tasks']}")
                print(f"      Messages: {project['total_messages']}")
                print(f"      Decisions: {project['total_decisions']}")
            else:
                print(f"   ❌ Failed to get project: {resp.status_code}")
        except Exception as e:
            print(f"   ❌ Error: {e}")

        # 5. Get agents
        print("\n5️⃣ Checking agents...")
        try:
            resp = await client.get(f"{BASE_URL}/api/v1/projects/{project_id}/agents", headers=headers)
            if resp.status_code == 200:
                agents = resp.json()
                print(f"   ✅ {len(agents)} agents created:")
                for agent in agents:
                    print(f"      - {agent['name']} ({agent['role']}): {agent['status']}")
            else:
                print(f"   ❌ Failed to get agents: {resp.status_code}")
        except Exception as e:
            print(f"   ❌ Error: {e}")

        # 6. Get tasks
        print("\n6️⃣ Checking tasks...")
        try:
            resp = await client.get(f"{BASE_URL}/api/v1/projects/{project_id}/tasks", headers=headers)
            if resp.status_code == 200:
                tasks = resp.json()
                print(f"   ✅ {len(tasks)} tasks created:")
                for task in tasks[:5]:  # Show first 5
                    print(f"      - {task['title']}: {task['status']}")
            else:
                print(f"   ❌ Failed to get tasks: {resp.status_code}")
        except Exception as e:
            print(f"   ❌ Error: {e}")

        # 7. Get messages
        print("\n7️⃣ Checking messages...")
        try:
            resp = await client.get(f"{BASE_URL}/api/v1/projects/{project_id}/messages", headers=headers)
            if resp.status_code == 200:
                messages = resp.json()
                print(f"   ✅ {len(messages)} messages:")
                for msg in messages[:3]:  # Show first 3
                    print(f"      - {msg['message_type']}: {msg['subject']}")
            else:
                print(f"   ❌ Failed to get messages: {resp.status_code}")
        except Exception as e:
            print(f"   ❌ Error: {e}")

        print("\n✅ Test completed!")


if __name__ == "__main__":
    asyncio.run(test_flow())

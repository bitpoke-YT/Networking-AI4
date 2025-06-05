import subprocess
import sys

def build_images():
    for i in range(1, 9):
        tag = f"flask-app-v{i}:latest"
        context = f"./V{i}"
        print(f"Building image {tag} from {context}...")
        subprocess.run([
            "docker", "build",
            "-t", tag,
            "--build-arg", "APP_FILE=Main.py",
            "-f", "Dockerfile",
            context
        ], check=True)
    print("All images built.")

def destroy_clab():
    try:
        subprocess.run(
            ["containerlab", "destroy", "-t", "topology.yml", "--cleanup"],
            check=True, capture_output=True
        )
        print("Previous lab destroyed.")
    except subprocess.CalledProcessError:
        print("No previous lab to destroy or error during destroy.")

def deploy_clab():
    subprocess.run(["containerlab", "deploy", "-t", "topology.yml"], check=True)
    print("Done Deploying")

if __name__ == "__main__":
    build_images()
    destroy_clab()
    deploy_clab()
    print("Done")
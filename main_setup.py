import subprocess
import os
import setup.setupV1
import setup.setupV2
import setup.setupV3
import setup.setupV4
import setup.setupV5
import setup.setupV6
import setup.setupV7
import setup.setupV8

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

def build_breach_image():
    print("Building image breach-app:latest from ./Breach...")
    subprocess.run([
        "docker", "build",
        "-t", "breach-app:latest",
        "-f", "Dockerfile",
        "./Breach"
    ], check=True)
    print("Breach image built.")

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

def run_setup(challenge_number):
    # Clear the screen
    if os.name == 'nt':  # Windows
        os.system('cls')
    else:  # Linux/Unix/MacOS
        os.system('clear')

    setup_function = getattr(setup, f"setupV{challenge_number}")
    setup_function.Setup()
    print(f"Setup for V{challenge_number} completed.")

def menu():
    print("Select an option:")
    print("1. Run setup for a specific challenge (1-8)")
    print("2. Run setup for all challenges (1-8)")
    choice = input("Enter your choice (1 or 2): ")

    if choice == "1":
        challenge_number = input("Enter the challenge number (1-8): ")
        if challenge_number.isdigit() and 1 <= int(challenge_number) <= 8:
            run_setup(int(challenge_number))
        else:
            print("Invalid challenge number. Please enter a number between 1 and 8.")
    elif choice == "2":
        for i in range(1, 9):
            run_setup(i)
    else:
        print("Invalid choice. Please enter 1 or 2.")

if __name__ == "__main__":
    build_images()
    build_breach_image()
    destroy_clab()
    deploy_clab()
    print("Done Clab")
    menu()
from login import login
import patientconnect_cli


def main():

    user = login()

    if user is None:
        print()
        print("Access denied.")
        return

    print()
    print("========================================")
    print("       PATIENT CONNECT DASHBOARD")
    print("========================================")
    print("User :", user["username"])
    print("Role :", user["role"])
    print("========================================")

    # Start your existing PatientConnect menu
    patientconnect_cli.main()


if __name__ == "__main__":
    main()
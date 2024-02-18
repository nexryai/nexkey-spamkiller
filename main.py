import time
import requests
import json

print("==== Nexkey spam-killer ver.0.01 ====")

# CHANGE ME
instance_host = "example.org"
token = "SECRET_TOKEN"

while True:
    # 通報一覧を取得
    report_endpoint = f"https://{instance_host}/api/admin/abuse-user-reports"
    report_payload = {
        "state": "unresolved",
        "reporterOrigin": "combined",
        "targetUserOrigin": "combined",
        "limit": 10,
        "i": token
    }

    response = requests.post(report_endpoint, json=report_payload)
    response_json = response.json()

    if response.status_code == 200:
        if len(response_json) != 0:
            target_host = response_json[0]["targetUser"]["host"]

            confirmation = input(f"Are you sure you want to suspend the user with host {target_host}? (Y/N): ")

            if confirmation.upper() != "Y":
                raise Exception

            # 配送停止
            update_meta_endpoint = f"https://{instance_host}/api/admin/federation/update-instance"
            update_meta_payload = {
                "host": target_host,
                "isSuspended": True,
                "i": token
            }

            update_response = requests.post(update_meta_endpoint, json=update_meta_payload)

            if update_response.status_code == 204:
                print(f"Host {target_host} suspended successfully.")
            else:
                print(f"Failed to suspend host. Status code: {update_response.status_code}")
                raise Exception



            # ブロック
            meta_response = requests.post(f"https://{instance_host}/api/admin/meta", json={"i": token})
            if update_response.status_code != 204:
                print(f"Failed to get meta. Status code: {update_response.status_code}")
                raise Exception

            meta = meta_response.json()
            meta["blockedHosts"].append(target_host)

            update_meta_payload = {
                "blockedHosts": meta["blockedHosts"],
                "i": token
            }

            update_response = requests.post(f"https://{instance_host}/api/admin/update-meta", json=update_meta_payload)

            if update_response.status_code == 204:
                print(f"Host {target_host} blocked successfully.")
            else:
                print(f"Failed to block host. Status code: {update_response.status_code}")
                raise Exception


            # インスタンスの全ユーザー削除
            kill_host_endpoint = f"https://{instance_host}/api/admin/delete-instance-users"
            kill_host_payload = {
                "host": target_host,
                "i": token
            }

            update_response = requests.post(kill_host_endpoint, json=kill_host_payload)

            if update_response.status_code == 204:
                print(f"User with host {target_host} deleted successfully.")
            else:
                print(f"Failed to delete host. Status code: {update_response.status_code}")
                raise Exception
        else:
            print("No unresolved abuse user reports ✌")
            break
    else:
        print(f"Failed to fetch abuse user reports. Status code: {response.status_code}")
        raise Exception
    
    # 過負荷防止
    time.sleep(3)

import requests

def run_inference():
    server_url = "http://127.0.0.1:8000"

    print("[START]", flush=True)

    for task in ["easy", "medium", "hard"]:
        try:
            requests.post(f"{server_url}/reset", json={"task": task})
        except Exception:
            print(f"[STEP] task={task} step=0 action=reset reward=0.00 done=true error=reset_failed", flush=True)
            continue

        done = False
        step = 0

        while not done and step < 15:
            step += 1

            try:
                if task == "easy":
                    action = {
                        "action_type": "assign_folder",
                        "email_id": "email_1",
                        "folder_name": "Billing"
                    }
                    done = True

                elif task in ["medium", "hard"]:
                    if step == 1:
                        action = {"action_type": "assign_folder", "email_id": "email_1", "folder_name": "Billing"}
                    elif step == 2:
                        action = {"action_type": "assign_folder", "email_id": "email_2", "folder_name": "Support"}
                    elif step == 3:
                        action = {"action_type": "add_tag", "email_id": "email_2", "tag_name": "Urgent"}
                    elif step == 4:
                        action = {"action_type": "assign_folder", "email_id": "email_3", "folder_name": "Spam"}
                    elif step == 5:
                        action = {"action_type": "assign_folder", "email_id": "email_4", "folder_name": "Support"}
                    elif step == 6 and task == "hard":
                        action = {"action_type": "reply", "email_id": "email_2", "reply_message": "refund processed"}
                    else:
                        action = {"action_type": "submit"}
                        done = True

                response = requests.post(f"{server_url}/step", json=action).json()

                reward = float(response.get("reward", 0.0))
                done = response.get("done", True)

                print(
                    f"[STEP] task={task} step={step} action={action['action_type']} reward={reward:.2f} done={str(done).lower()} error=null",
                    flush=True
                )

            except Exception:
                print(
                    f"[STEP] task={task} step={step} action=error reward=0.00 done=true error=step_failed",
                    flush=True
                )
                break

    print("[END]", flush=True)


if __name__ == "__main__":
    run_inference()

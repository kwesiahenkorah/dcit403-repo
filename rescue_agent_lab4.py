from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
import asyncio
import time

class RescueAgent(Agent):
    class RescueBehaviour(CyclicBehaviour):
        async def run(self):
            msg = await self.receive(timeout=10)

            if msg:
                performative = msg.get_metadata("performative")
                ontology = msg.get_metadata("ontology")
                body = msg.body

                print("\n--- RescueAgent Received Message ---")
                print(f"From: {msg.sender}")
                print(f"Performative: {performative}")
                print(f"Ontology: {ontology}")
                print(f"Body: {body}")

                with open("lab4_message_log.txt", "a") as file:
                    file.write(f"RESCUE RECEIVED | {performative} | {body}\n")

                # Parse and trigger action
                if performative == "request" and ontology == "rescue-task":
                    task, timestamp, severity = body.split("|")

                    print(f"\n[ACTION] Executing task: {task}")
                    print(f"Timestamp: {timestamp}")
                    print(f"Severity: {severity}")
                    print("Rescue operation in progress...")

                    time.sleep(3)

                    print("Rescue operation completed.\n")
                    with open("lab4_message_log.txt", "a") as file:
                        file.write(f"RESCUE ACTION COMPLETED | {timestamp} | {severity}\n")

            else:
                print("RescueAgent waiting...")

    async def setup(self):
        print(f"RescueAgent {self.jid} starting...")
        self.add_behaviour(self.RescueBehaviour())


async def main():
    jid = "rescueagent99@xmpp.jp"
    password = "Kwesi316"

    agent = RescueAgent(jid, password)
    await agent.start()
    print("RescueAgent running...")

    try:
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        print("\nStopping RescueAgent...")
        await agent.stop()

if __name__ == "__main__":
    asyncio.run(main())

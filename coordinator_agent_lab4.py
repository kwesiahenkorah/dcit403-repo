from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.message import Message
import asyncio

class CoordinatorAgent(Agent):
    class ReceiveAndDispatchBehaviour(CyclicBehaviour):
        async def run(self):
            msg = await self.receive(timeout=10)

            if msg:
                performative = msg.get_metadata("performative")
                ontology = msg.get_metadata("ontology")
                body = msg.body

                print("\n--- Coordinator Received Message ---")
                print(f"From: {msg.sender}")
                print(f"Performative: {performative}")
                print(f"Ontology: {ontology}")
                print(f"Body: {body}")

                # log
                with open("lab4_message_log.txt", "a") as file:
                    file.write(f"COORDINATOR RECEIVED | {performative} | {body}\n")

                # Parse sensor report
                if performative == "inform" and ontology == "disaster-report":
                    timestamp, severity = body.split("|")

                    # Decision rule: request rescue only for HIGH or CRITICAL
                    if severity in ["HIGH", "CRITICAL"]:
                        request = Message(to=self.agent.rescue_jid)
                        request.set_metadata("performative", "request")
                        request.set_metadata("ontology", "rescue-task")
                        request.body = f"RESCUE|{timestamp}|{severity}"

                        await self.send(request)

                        print(f"REQUEST sent to RescueAgent -> {severity}")
                        with open("lab4_message_log.txt", "a") as file:
                            file.write(f"COORDINATOR -> RESCUE | REQUEST | {request.body}\n")
                    else:
                        print("No rescue request sent (severity too low).")

            else:
                print("Coordinator waiting...")

    async def setup(self):
        print(f"CoordinatorAgent {self.jid} starting...")
        self.rescue_jid = "rescueagent99@xmpp.jp"  
        self.add_behaviour(self.ReceiveAndDispatchBehaviour())


async def main():
    jid = "coordinatoragent99@xmpp.jp"   
    password = "Kwesi316"

    agent = CoordinatorAgent(jid, password)
    await agent.start()
    print("CoordinatorAgent running...")

    try:
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        print("\nStopping CoordinatorAgent...")
        await agent.stop()

if __name__ == "__main__":
    asyncio.run(main())

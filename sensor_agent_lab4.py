from spade.agent import Agent
from spade.behaviour import PeriodicBehaviour
from spade.message import Message
import asyncio
from environment import DisasterEnvironment

class SensorAgent(Agent):
    class SenseBehaviour(PeriodicBehaviour):
        async def run(self):
            event = self.environment.sense()
            severity = event["severity"]
            timestamp = event["timestamp"]

            log_entry = f"[{timestamp}] Disaster detected | Severity: {severity}"
            print(log_entry)

            # log locally
            with open("lab4_message_log.txt", "a") as file:
                file.write(f"SENSOR LOG: {log_entry}\n")

            # INFORM CoordinatorAgent
            msg = Message(to=self.coordinator_jid)
            msg.set_metadata("performative", "inform")
            msg.set_metadata("ontology", "disaster-report")
            msg.body = f"{timestamp}|{severity}"

            await self.send(msg)

            print(f"INFORM sent to Coordinator -> {severity}")
            with open("lab4_message_log.txt", "a") as file:
                file.write(f"SENSOR -> COORDINATOR | INFORM | {msg.body}\n")

        async def on_start(self):
            print("SensorAgent started sensing environment...")

    async def setup(self):
        self.environment = DisasterEnvironment()
        self.coordinator_jid = "coordinatoragent99@xmpp.jp"  

        behaviour = self.SenseBehaviour(period=5)
        behaviour.environment = self.environment
        behaviour.coordinator_jid = self.coordinator_jid
        self.add_behaviour(behaviour)


async def main():
    jid = "sensoragent@xmpp.jp"
    password = "Kwesi316"

    agent = SensorAgent(jid, password)
    await agent.start()
    print(f"SensorAgent {jid} started successfully!")

    try:
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        print("\nStopping SensorAgent...")
        await agent.stop()
        print("SensorAgent stopped.")

if __name__ == "__main__":
    asyncio.run(main())

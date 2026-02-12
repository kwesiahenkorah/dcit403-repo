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

            # Save to log file
            with open("event_log.txt", "a") as file:
                file.write(log_entry + "\n")

            # Send alert to RescueAgent if severity is MODERATE or higher
            if severity in ["MODERATE", "HIGH", "CRITICAL"]:
                msg = Message(to=self.rescue_jid)
                msg.set_metadata("performative", "inform")
                msg.set_metadata("ontology", "disaster-alert")
                msg.body = f"{timestamp}|{severity}"

                await self.send(msg)
                print(f"Alert sent to RescueAgent -> {severity}")

        async def on_start(self):
            print("SensorAgent started sensing environment...")

    async def setup(self):
        self.environment = DisasterEnvironment()

        # Set who receives alerts
        self.rescue_jid = "rescueagent@xmpp.jp"  # change if needed

        behaviour = self.SenseBehaviour(period=5)
        behaviour.environment = self.environment
        behaviour.rescue_jid = self.rescue_jid

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

from spade.agent import Agent
from spade.behaviour import PeriodicBehaviour
import asyncio
from environment import DisasterEnvironment

class SensorAgent(Agent):
    class SenseBehaviour(PeriodicBehaviour):
        async def run(self):
            event = self.environment.sense()
            log_entry = (
                f"[{event['timestamp']}] "
                f"Disaster detected | Severity: {event['severity']}"
            )
            print(log_entry)

            # Save to log file
            with open("event_log.txt", "a") as file:
                file.write(log_entry + "\n")

        async def on_start(self):
            print("SensorAgent started sensing environment...")

    async def setup(self):
        self.environment = DisasterEnvironment()
        behaviour = self.SenseBehaviour(period=5)  # sense every 5 seconds
        behaviour.environment = self.environment
        self.add_behaviour(behaviour)


async def main():
    jid = "sensoragent@xmpp.jp"       
    password = "Kwesi316"             

    agent = SensorAgent(jid, password)
    
    # Start the agent
    await agent.start()
    print(f"Agent {jid} started successfully!")
    
    try:
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        print("\nStopping agent...")
        await agent.stop()
        print("Agent stopped.")

if __name__ == "__main__":
     asyncio.run(main())
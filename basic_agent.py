from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
import asyncio

class HelloAgent(Agent):
    class HelloBehaviour(CyclicBehaviour):
        async def run(self):
            print(f"Agent {self.agent.jid} is running...")
            await asyncio.sleep(5)

    async def setup(self):
        print(f"{self.jid} starting...")
        self.add_behaviour(self.HelloBehaviour())

async def main():
    jid = "sensoragent@xmpp.jp"  
    password = "Kwesi316"    

    agent = HelloAgent(jid, password)
    await agent.start()

    try:
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        await agent.stop()

if __name__ == "__main__":
    asyncio.run(main())

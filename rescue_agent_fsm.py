from spade.agent import Agent
from spade.behaviour import FSMBehaviour, State
from spade.message import Message
import asyncio
import time

# FSM State Names
STATE_IDLE = "IDLE"
STATE_ASSESS = "ASSESS"
STATE_DISPATCH = "DISPATCH"
STATE_COMPLETE = "COMPLETE"

class RescueAgent(Agent):

    class RescueFSM(FSMBehaviour):
        async def on_start(self):
            print("RescueAgent FSM started.")

        async def on_end(self):
            print("RescueAgent FSM finished.")

    # STATE 1: IDLE
    class IdleState(State):
        async def run(self):
            print("\n[STATE] IDLE: Waiting for disaster alert...")

            msg = await self.receive(timeout=10)
            if msg:
                self.agent.last_alert = msg.body
                print(f"Received alert: {msg.body}")
                self.set_next_state(STATE_ASSESS)
            else:
                print("No alert received. Staying idle.")
                self.set_next_state(STATE_IDLE)

    # STATE 2: ASSESS
    class AssessState(State):
        async def run(self):
            print("\n[STATE] ASSESS: Evaluating disaster severity...")

            timestamp, severity = self.agent.last_alert.split("|")

            self.agent.current_severity = severity
            print(f"Timestamp: {timestamp}")
            print(f"Severity: {severity}")

            # Decision rule
            if severity in ["HIGH", "CRITICAL"]:
                self.set_next_state(STATE_DISPATCH)
            else:
                print("Severity not high enough for rescue dispatch.")
                self.set_next_state(STATE_IDLE)

    # STATE 3: DISPATCH
    class DispatchState(State):
        async def run(self):
            print("\n[STATE] DISPATCH: Sending rescue team...")

            severity = self.agent.current_severity
            print(f"Rescue operation started for severity: {severity}")

            # Simulated rescue time
            time.sleep(3)

            self.set_next_state(STATE_COMPLETE)

    # STATE 4: COMPLETE
    class CompleteState(State):
        async def run(self):
            print("\n[STATE] COMPLETE: Rescue operation finished.")
            print("Returning to IDLE state...")

            self.set_next_state(STATE_IDLE)

    async def setup(self):
        print(f"RescueAgent {self.jid} starting...")

        fsm = self.RescueFSM()

        fsm.add_state(name=STATE_IDLE, state=self.IdleState(), initial=True)
        fsm.add_state(name=STATE_ASSESS, state=self.AssessState())
        fsm.add_state(name=STATE_DISPATCH, state=self.DispatchState())
        fsm.add_state(name=STATE_COMPLETE, state=self.CompleteState())

        fsm.add_transition(source=STATE_IDLE, dest=STATE_IDLE)
        fsm.add_transition(source=STATE_IDLE, dest=STATE_ASSESS)
        fsm.add_transition(source=STATE_ASSESS, dest=STATE_IDLE)
        fsm.add_transition(source=STATE_ASSESS, dest=STATE_DISPATCH)
        fsm.add_transition(source=STATE_DISPATCH, dest=STATE_COMPLETE)
        fsm.add_transition(source=STATE_COMPLETE, dest=STATE_IDLE)

        self.add_behaviour(fsm)


async def main():
    jid = "rescueagent99@xmpp.jp"   
    password = "Kwesi316"        

    agent = RescueAgent(jid, password)
    await agent.start()

    print("RescueAgent is running. Press CTRL+C to stop.")
    try:
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        print("\nStopping RescueAgent...")
        await agent.stop()

if __name__ == "__main__":
    asyncio.run(main())

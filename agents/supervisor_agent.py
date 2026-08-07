from datetime import datetime


class SupervisorAgent:


    """
    Supervisor Agent ORION v3

    Fungsi:
    - observasi sistem
    - adaptive learning
    - pengambilan keputusan
    - penyimpanan pengalaman
    """



    def __init__(

        self,
        kernel=None,
        memory=None,
        adaptive=None

    ):


        self.kernel = kernel

        self.memory = memory

        self.adaptive = adaptive


        self.status = "initialized"

        self.cycle = 0



        print(
            "SUPERVISOR AGENT ONLINE"
        )





    # ==========================
    # OBSERVE
    # ==========================


    def observe(self):


        self.cycle += 1



        observation = {


            "cycle":

            self.cycle,


            "time":

            datetime.now().isoformat(),



            "kernel":

            self.kernel.state

            if self.kernel

            else None


        }



        if self.memory:


            self.memory.remember(

                "supervisor_observation",

                observation

            )



        return observation






    # ==========================
    # ADAPTIVE ANALYSIS
    # ==========================


    def learn(

        self,
        observation

    ):


        if not self.adaptive:


            return None



        result = self.adaptive.analyze(

            {

                "goal":

                "system_monitoring",


                "step":

                str(observation)

            }

        )



        return result







    # ==========================
    # DECIDE
    # ==========================


    def decide(

        self,
        observation

    ):


        if not observation:


            return {


                "action":

                "wait",


                "reason":

                "no observation"

            }




        learning = self.learn(

            observation

        )



        decision = {


            "action":

            "continue",



            "reason":

            "system healthy",



            "cycle":

            observation["cycle"],



            "learning":

            learning


        }





        if self.memory:


            self.memory.remember(

                "supervisor_decision",

                decision

            )



        return decision







    # ==========================
    # RUN
    # ==========================


    def run_once(self):


        observation = self.observe()



        decision = self.decide(

            observation

        )



        return {


            "observation":

            observation,



            "decision":

            decision

        }

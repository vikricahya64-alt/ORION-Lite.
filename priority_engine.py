class PriorityEngine:


    def evaluate(self, action, owner_request=False):

        if owner_request:

            return {
                "priority": 5,
                "reason": "Permintaan pemilik"
            }


        rules = {

            "task": {
                "priority": 5,
                "reason": "Pekerjaan aktif"
            },

            "learning": {
                "priority": 4,
                "reason": "Pengembangan pengetahuan"
            },

            "ai": {
                "priority": 3,
                "reason": "Proses AI umum"
            },

            "cleanup": {
                "priority": 1,
                "reason": "Pemeliharaan sistem"
            }

        }


        return rules.get(
            action,
            {
                "priority": 2,
                "reason": "Prioritas standar"
            }
        )

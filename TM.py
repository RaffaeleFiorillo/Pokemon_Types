common_degree = {"Fire": 92/1532, "Ice": 52/1532, "Bug": 88/1532, "Poison": 78/1532, "Fighting": 72/1532,
                 "Rock": 72/1532, "Fairy": 61/1532, "Dragon": 64/1532, "Dark": 69/1532, "Ghost": 61/1532,
                 "Normal": 126/1532, "Electric": 70/1532, "Flying": 113/1532, "Steel": 67/1532, "Grass": 116/1532,
                 "Water": 148/1532, "Ground": 74/1532, "Psychic": 109/1532}

total_pokemon_number = sum([value for value in common_degree.values()])
print(f"Total pokemon number: {total_pokemon_number}\n ----------------------------")

def ordering_function(pair_values):
    value = pair_values[1]
    if value == 0:
        return 5
    return value

class Type:
    def __init__(self, n_i, w_i, r_i):
        self.name = n_i
        self.resists = r_i
        self.weak = w_i


class Type_Combo:
    def __init__(self, t1, t2):
        self.name = None  # unique identification. Describes the two types combined
        self.strength: float = 0  # the strategic value of this combination of types
        self.weaknesses: dict = {}  # key: type; value: multiplier (ex: 2 -> double damage)
        self.resistances = {}  # key: type; value: multiplier (ex: 2 -> half damage)
        self.create(t1, t2)  # creates the previous attributes

    def create(self, t1, t2):
        self.name = f"{t1.name} | {t2.name}"
        self.weaknesses = self.add_attributes(t1.weak, t2.weak)
        self.resistances = self.add_attributes(t1.resists, t2.resists)
        self.sum_w_r()  # if a type_1 is strong against type_x, but type_2 is weak against it, they nullify each other
        self.calculate_strength()

    def sum_w_r(self):
        w_i, r_i = self.weaknesses.copy(), self.resistances.copy()
        for a_key in self.resistances:
            # if type1 is strong and type2 is weak and it doesnt
            if a_key in self.weaknesses and a_key in self.resistances:
                w_i.pop(a_key)
                r_i.pop(a_key)
                if self.resistances[a_key] == 0:  # if it takes 0 damage from a type, the combination will also take 0
                    r_i[a_key] = 0
        self.weaknesses, self.resistances = w_i, r_i

    @staticmethod
    def add_type(a, t):
        if (t_n:=t.strip("*")) in a:
            if t[-1] == "*":  # A type which causes 0 damage is marked with an "*"
                a[t_n] = 0
            elif a[t]:  # Damage is added only if, for this type, damage taken is not 0
                a[t] += 2
        else:  # if type doesn't exist yet, it is initialized as 2
            if t[-1] == "*":  # A type which causes 0 damage is marked with an "*"
                a[t_n] = 0
            else:
                a[t] = 2
        return a

    def add_attributes(self, a1, a2):
        a_combo = {}
        for type_1 in a1:
            self.add_type(a_combo, type_1)
        for type_2 in a2:
            self.add_type(a_combo, type_2)
        a_combo = sorted(a_combo.items(), key=lambda x: ordering_function(x))  # sort dictionary based on values
        a_combo = dict(a_combo)
        return a_combo

    def display_attributes(self):
        print("\n -------------------------")
        print(f"Type: {self.name}")
        print(f"Power: {self.strength}")
        print(f"Weak Against ({len(self.weaknesses)}): \n\t{self.weaknesses}")
        print(f"Resistant Against ({len(self.resistances)}): \n\t{self.resistances}")
        print("-------------------------\n")

    @staticmethod
    def compute_value(characteristics: dict):
        value = 0
        for type_c, value_c in characteristics.items():
            value += value_c*common_degree[type_c]
        return value

    def count_r_zeros(self):
        return sum([1 if not res else 0 for res in self.resistances.values()])

    def count_w_fours(self):
        return sum([1 if res==4 else 0 for res in self.weaknesses.values()])

    def calculate_strength(self):
        # Weakness Contribution ----------------------------------------------------------------------------------------
        # 16-> maximum weakness value | 2-> minimum | normalizing formula-> 1 - (x-min)/(max-min)
        w_v = 1 - (self.compute_value(self.weaknesses) - 2) / 14  # combined value of weaknesses

        # 7-> maximum number of weaknesses | 1-> minimum | normalizing formula-> 1 - (x-min)/(max-min)
        w_l = 1- (len(self.weaknesses)-1)/6

        # 2-> maximum 4x weaknesses | 0-> minimum | normalizing formula-> 1- (x-min)/(max-min)
        w_f = 1 - self.count_w_fours()/2  # number of types which cause 4x damage to this combination

        w_total = w_v*0.5 + w_l*0.2 + w_f*0.3

        # Resistance Contribution --------------------------------------------------------------------------------------
        # 28-> maximum weakness value | 0-> minimum | normalizing formula-> (x-min)/(max-min)
        r_v = self.compute_value(self.resistances)/28  # combined value of resistances

        # 12-> maximum number of resistances | 1-> minimum | normalizing formula-> (x-min)/(max-min)
        r_l = (len(self.resistances)-1)/11  #

        # 3-> maximum weakness value | 0-> minimum | normalizing formula-> (x-min)/(max-min)
        r_z = self.count_r_zeros()/3  # number of types which cause zero damage to this combination

        r_total = r_v*0.5 + r_l*0.2 + r_z*0.3

        # total strength-> w_total:50% | r_total:50% -------------------------------------------------------------------
        self.strength = round(w_total*0.5+r_total*0.5, 4)


# Fire ------------------
n = "Fire"
w = ["Ground", "Rock", "Water"]
r = ["Bug", "Steel", "Ice", "Fairy", "Grass", "Fire"]
Fire = Type(n, w, r)

# Ice -----------------------
n = "Ice"
w = ["Fighting", "Rock", "Steel", "Fire"]
r = ["Ice"]
Ice = Type(n, w, r)

# Fairy -----------------
n = "Fairy"
w = ["Poison", "Steel"]
r = ["Fighting", "Bug", "Dragon*", "Dark"]
Fairy = Type(n, w, r)

# Steel ----------------
n = "Steel"
w = ["Fighting", "Ground", "Fire"]
r = ["Normal", "Flying", "Poison*", "Rock", "Bug", "Steel", "Grass", "Psychic", "Ice", "Dragon", "Fairy"]
Steel = Type(n, w, r)

# Dark -----------------
n = "Dark"
w = ["Fighting", "Bug", "Fairy"]
r = ["Ghost", "Psychic*", "Dark"]
Dark = Type(n, w, r)

# Ghost ---------------
n = "Ghost"
w = ["Ghost", "Dark"]
r = ["Normal*", "Fighting*", "Poison", "Bug"]
Ghost = Type(n, w, r)

# Psychic ------------
n = "Psychic"
w = ["Bug", "Ghost", "Dark"]
r = ["Fighting", "Psychic"]
Psychic = Type(n, w, r)

# Electric -------------
n = "Electric"
w = ["Ground"]
r = ["Flying", "Steel", "Electric"]
Electric = Type(n, w, r)

# Ground --------------
n = "Ground"
w = ["Water", "Grass", "Ice"]
r = ["Poison", "Rock", "Electric*"]
Ground = Type(n, w, r)

# Grass -----------------
n = "Grass"
w = ["Flying", "Poison", "Bug", "Fire", "Ice"]
r = ["Ground", "Water", "Grass", "Electric"]
Grass = Type(n, w, r)

# Water -----------------
n = "Water"
w = ["Grass", "Electric"]
r = ["Steel", "Fire", "Water", "Ice"]
Water = Type(n, w, r)

# Flying -----------------
n = "Flying"
w = ["Rock", "Electric", "Ice"]
r = ["Fighting", "Ground*", "Bug", "Grass"]
Flying = Type(n, w, r)

# Dragon ---------------
n = "Dragon"
w = ["Dragon", "Fairy", "Ice"]
r = ["Fire", "Water", "Grass", "Electric"]
Dragon = Type(n, w, r)

# Normal ---------------
n = "Normal"
w = ["Fighting"]
r = ["Ghost"]
Normal = Type(n, w, r)

# Rock -------------------
n = "Rock"
w = ["Fighting", "Ground", "Steel", "Water", "Grass"]
r = ["Normal", "Flying", "Poison", "Fire"]
Rock = Type(n, w, r)

# Fighting --------------
n = "Fighting"
w = ["Flying", "Psychic", "Fairy"]
r = ["Rock", "Bug", "Dark"]
Fighting = Type(n, w, r)

# Poison ----------------
n = "Poison"
w = ["Ground", "Psychic"]
r = ["Fighting", "Poison", "Bug", "Grass", "Fairy"]
Poison = Type(n, w, r)

# Bug ---------------------
n = "Bug"
w = ["Flying", "Rock", "Fire"]
r = ["Fighting", "Ground", "Grass"]
Bug = Type(n, w, r)


P_Types = [Fire, Ice, Bug, Poison, Fighting, Rock, Fairy, Dragon, Dark, Ghost, Normal, Electric, Flying, Steel, Grass,
           Water, Ground, Psychic]

P_Types = [Fighting, Dragon, Dark, Ghost, Electric, Steel]

# returns a list of all possible types combinations sorted in ascending order of strength
def create_all_possible_types(p_t: [Type])-> [Type_Combo]:
    types = []
    for i, t1 in enumerate(p_t):
        for t2 in p_t[i + 1:]:
            types.append(Type_Combo(t1, t2))
    types.sort(key=lambda pt: pt.strength)
    return types

def search_combo(type1: str, type2: str)-> Type_Combo:
    for type_x in P_Types:
        if type1 in type_x.name and type2 in type_x.name:
            return type_x


COMBOS = create_all_possible_types(P_Types)

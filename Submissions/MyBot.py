# bot code goes here
from Game.Skills import *
from Game.projectiles import *
from ScriptingHelp.usefulFunctions import *
from Game.playerActions import defense_actions, attack_actions, projectile_actions
from Game.gameSettings import HP, LEFTBORDER, RIGHTBORDER, LEFTSTART, RIGHTSTART, PARRYSTUN

# PRIMARY CAN BE: Teleport, Super Saiyan, Meditate, Dash Attack, Uppercut, One Punch
# SECONDARY CAN BE : Hadoken, Grenade, Boomerang, Bear Trap

# TODO FOR PARTICIPANT: Set primary and secondary skill here
PRIMARY_SKILL = Meditate
SECONDARY_SKILL = SuperSaiyanSkill

# constants, for easier move return
# movements
JUMP = ("move", (0, 1))
FORWARD = ("move", (1, 0))
BACK = ("move", (-1, 0))
JUMP_FORWARD = ("move", (1, 1))
JUMP_BACKWARD = ("move", (-1, 1))

# attacks and block
LIGHT = ("light",)
HEAVY = ("heavy",)
BLOCK = ("block",)

PRIMARY = get_skill(PRIMARY_SKILL)
SECONDARY = get_skill(SECONDARY_SKILL)
CANCEL = ("skill_cancel",)

# no move, aka no input
NOMOVE = "NoMove"
# for testing
moves = SECONDARY,
moves_iter = iter(moves)


# TODO FOR PARTICIPANT: WRITE YOUR WINNING BOT
class Script:
    def __init__(self):
        self.primary = PRIMARY_SKILL
        self.secondary = SECONDARY_SKILL

        self.time = 0
        self.block_heavy = False

    # DO NOT TOUCH
    def init_player_skills(self):
        return self.primary, self.secondary

    # MAIN FUNCTION that returns a single move to the game manager
    def get_move(self, player, enemy, player_projectiles, enemy_projectiles):
        self.time += 1
        distance = abs(get_pos(player)[0] - get_pos(enemy)[0])

        # if distance < 2 and not get_stun_duration(enemy):

        if enemy_projectiles:
            proj_dist = abs(get_pos(player)[0] - get_proj_pos(enemy_projectiles[0])[0])
            if get_projectile_type(enemy_projectiles[0]) == "hadoken":
                if proj_dist <= 3:
                    print("block")
                    return BLOCK
                elif proj_dist == 3:
                    return JUMP
            elif get_projectile_type(enemy_projectiles[0]) == "grenda" and proj_dist < 3:
                return JUMP_FORWARD
            # elif get_projectile_type(enemy_projectiles[0]) ==

        if (get_hp(player) <= 80 or self.time > 125) and not primary_on_cooldown(player):
            return PRIMARY

        if not secondary_on_cooldown(player):
            return SECONDARY  # jump and using sai ya

        if distance < 2:
            if not heavy_on_cooldown(player):
                return HEAVY
            return LIGHT

        return FORWARD

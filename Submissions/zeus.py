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

#constants, for easier move return
#movements
JUMP = ("move", (0,1))
FORWARD = ("move", (1,0))
BACK = ("move", (-1,0))
JUMP_FORWARD = ("move", (1,1))
JUMP_BACKWARD = ("move", (-1, 1))

# attacks and block
LIGHT = ("light",)
HEAVY = ("heavy",)
BLOCK = ("block",)

PRIMARY = get_skill(PRIMARY_SKILL)
SECONDARY = get_skill(SECONDARY_SKILL)
CANCEL = ("skill_cancel", )

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
        self.clock = 0
        self.count_down = 0
        self.conflict = 0
        
    # DO NOT TOUCH
    def init_player_skills(self):
        return self.primary, self.secondary
    
    def dogde_from_projectile(self,player_pos,enemy_projectiles):
        if enemy_projectiles is not None:
            for enemy_projectile in enemy_projectiles:
                dist_danger=abs(player_pos[0]-get_proj_pos(enemy_projectile)[0])
                if dist_danger<=1:
                    return True
        return False

    def need_block(self,player,enemy):
        enemy_last_act1=get_past_move(enemy,1)
        enemy_last_act2=get_past_move(enemy,2)
        if (enemy_last_act1 in [LIGHT,HEAVY]) and (enemy_last_act2 in [LIGHT,HEAVY]):
            return True
        else:
            return False
    
    def combo_a(self,player, enemy):
        # print(heavy_on_cooldown(player))
        if not heavy_on_cooldown(player):
            return HEAVY
        return LIGHT
    
    # Mediate & Super Saiyan
    def strategy_1(self,player, enemy, player_projectiles, enemy_projectiles):
        player_hp=get_hp(player)
        enemy_hp=get_hp(enemy)
        player_pos=get_pos(player)
        enemy_pos=get_pos(enemy)
        player_last_act=get_last_move(player)
        enemy_last_act=get_last_move(enemy)
        print(player_last_act,enemy_last_act)
        distance = abs(player_pos[0] - enemy_pos[0])

        # print(get_primary_cooldown(player),get_secondary_cooldown(player))
        if self.dogde_from_projectile(player_pos,enemy_projectiles):
            return JUMP
        if (not primary_on_cooldown(player) and player_hp<=80) or self.clock>110:
            return PRIMARY
        else:
            if distance>=2:
                if distance==2:
                    if enemy_last_act=='move' and player_last_act=='move':
                        return LIGHT
                    self.count_down=1
                return FORWARD
            elif distance<2:
                if self.count_down:
                    self.count_down-=1
                    return BLOCK
                if not secondary_on_cooldown(player):
                    return SECONDARY
                else:
                    return self.combo_a(player,enemy)
    
    # dash & super saiyan
    def strategy_2(self,player, enemy, player_projectiles, enemy_projectiles):
        player_hp=get_hp(player)
        enemy_hp=get_hp(enemy)
        player_pos=get_pos(player)
        enemy_pos=get_pos(enemy)

        distance = abs(player_pos[0] - enemy_pos[0])
        # print(get_primary_cooldown(player),get_secondary_cooldown(player))
        if self.dogde_from_projectile(player_pos,enemy_projectiles):
            return JUMP
        
        if distance>5:
            return FORWARD
        elif distance>=2:
            if not get_primary_cooldown(player):
                return PRIMARY
            else:
                return FORWARD
        else:
            if not get_secondary_cooldown(player):
                return SECONDARY
            else:
                return self.combo_a(player, enemy)
    
    # MAIN FUNCTION that returns a single move to the game manager
    def get_move(self, player, enemy, player_projectiles, enemy_projectiles):
        # add if-else here,depend on enemy's skill
        # print(get_last_move(player))
        self.clock+=1
        # if get_primary_skill(enemy)=='meditate' and get_secondary_skill(enemy)=='super_saiyan':
        #     return self.strategy_1(player, enemy, player_projectiles, enemy_projectiles)
        return self.strategy_1(player, enemy, player_projectiles, enemy_projectiles) 
        
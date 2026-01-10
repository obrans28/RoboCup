class Attacker:
    def decide(self, world_state):
        if world_state.ball_position:
            # Move towards ball
            target = world_state.ball_position
            return target
        else:
            # Go to center
            return (0.5, 0.45)

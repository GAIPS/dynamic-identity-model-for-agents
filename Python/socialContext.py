class SocialContext:
    def __init__(self, agentsPresent, theme):
        #agents present in the current context
        self.agentsPresent = agentsPresent
        #collection of the characteristics present in the theme (each one with a name and a weight 0 to 1)
        self.theme = theme

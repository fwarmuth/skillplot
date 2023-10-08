import matplotlib.pyplot as plt

class Barplot:
    """A class to create a github style skill plot.
    
    Attributes:
        skills (list): A list of strings representing skills.
        skill_levels (list): A list of integers representing skill levels.
    """
    def __init__(self, skills, skill_levels):
        """Initialize the SkillPlot class.
        
        Args:
            skills (list): A list of strings representing skills.
            skill_levels (list): A list of integers representing skill levels.
        """
        self.skills = skills
        self.skill_levels = skill_levels
    
    def plot(self):
        """Plot the skill plot.
        
        Returns:
            matplotlib.pyplot.figure: A matplotlib.pyplot.figure object.
        """
        # Set up the figure
        fig = plt.figure(figsize=(10, 10))
        ax = fig.add_subplot(1, 1, 1)
        
        # Plot the skill levels
        ax.barh(self.skills, self.skill_levels)
        
        # Set the x-axis limits
        ax.set_xlim([0, 10])
        
        # Set the y-axis labels
        ax.set_yticklabels(self.skills)
        
        # Set the x-axis labels
        ax.set_xlabel('Skill Level')
        
        # Set the title
        ax.set_title('My Skills')
        
        # Return the figure
        return fig
    
    def save(self, filename):
        """Save the skill plot to a file.
        
        Args:
            filename (str): The filename to save the skill plot to.
        """
        fig = self.plot()
        fig.savefig(filename)

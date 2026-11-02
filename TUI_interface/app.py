from textual.app import App, ComposeResult
from textual.widgets import Footer, Header, Button, Static
from textual.containers import Horizontal, Vertical

#These templates use for screen changing on pomodoro container when press menu button
# các class này kế thừa Vertical not App
#chúng là các tổ hợp các widgets được viễn sẵn thôi

#------------------------------------------

class PomodoroView(Vertical):
    def compose(self):
        yield Static("Pomodoro view")

class SubjectsView(Vertical):
    def compose(self):
        yield Static("Subjects view")

class PlansView(Vertical):
    def compose(self):
        yield Static("Plans view")

class SummaryView(Vertical):
    def compose(self):
        yield Static("Summary view")


#-------------------------------------------    

button_registry = {
    "btn-pomodoro" : PomodoroView,
    "btn-subjects" : SubjectsView,
    "btn-plans"    : PlansView
}

#-------------------------------------------

class Personal_Study_Planner(App):
    CSS_PATH="interface.tcss"

    #This is initial state when launch the TUI interface 
    
    def compose(self):
        yield Header()
        with Horizontal():
            with Vertical(id="menu"):

                yield Static("MENU")
                
                yield Button ('Exit',id="btn-exit")
                
                yield Button ("Pomodoro timer",id="btn-pomodoro")
                
                yield Button ("Subjects",id="btn-subjects")

                yield Button ("Plans", id="btn-plans")

                yield Button ("Summary", id="btn-summary")
                
            with Vertical(id="right"):
                
                with Vertical(id="pomodoro"):
                
                    yield Static("POMODORO")
                
                with Vertical(id="task"):
                
                    yield Static("TASK")
                    
        yield Footer()
    
    
    #pomodoro is a name for container that switch content when button on the
    #menu is pressed 
    
    async def update_pomodoro(self, template):
        container=self.query_one("#pomodoro", Vertical)
        await container.remove_children()
        await container.mount(template)

    async def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id =="btn-exit":
            self.exit()
        if event.button.id in button_registry:
                template_class = button_registry[event.button.id]
                await self.update_pomodoro(template_class())

if __name__ == '__main__':
    app= Personal_Study_Planner()
    app.run()
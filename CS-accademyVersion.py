#The code below is only ready to be perfomed in CS-Academy inbuilt IDE in the web-browser
#Math import was imported in order to calculate values using trigonometry
import math as m 

#Gravitational acceleration
grav_acc = 9.82
#Global variable throughout the application which is set default to 0 (Object Not Moving) but changes dependant on the inputed values
app.acceleration = 0
#How quickly I call the onStep() function in the program; set at 60 since 60FPS
app.stepsPerSecond = 60
#Global variable throught the application which shows how much time has progressed throught the simulation
app.time = 0
#Global variable throught the application which shows how high the velocity of the object is throughout the simulation
app.velocity = 0


#The Class where the physics calculations such forces in play are calculated
class Physics:
    def __init__(self, mass, degree, friction_num):
        #Initialisation of the different values that we get in input
        self.mass = mass #Inputed Mass
        self.degree = degree #Inputed Angle
        self.friction_num = friction_num #Inputed friction-coeffecient
    
    #Class method that calculate the magnituide of the different forces in play    
    def Force(self):
        
        #Code that checks if inputed values are valid
        if 0 >= self.degree or self.degree > 45: #Reason to deciding that 45 is the max is due to purely aesthetic and graphical reasons                                   
            return False
        if self.mass <= 0: #Can't do physics without mass (at least for now)
            return False

        else: 
            self.degree = m.radians(self.degree) #Converts the inputed degree of the triangle into radians since the math import uses radians
            #Calculates the gravitional force
            self.grav_force = grav_acc * self.mass 
            #Calculates the composant of the gravitional force that is parallell to the plane
            self.grav_force1 = abs(self.grav_force * m.sin(self.degree)) 
            #Calculates the composant of the gravitional force that is adjacent to the plane
            self.grav_force2 = self.grav_force * m.cos(self.degree)
            #Calculates the friction force the object resists against
            self.friction_force = abs(self.grav_force2 *  self.friction_num)
            #Calculates the netforce on the "horisontell" plane as in the plane the object travels
            self.netforce = self.grav_force1 - self.friction_force
            #Checks if the netforce is negative or equal to 0; if yes then returns friction string
            if self.netforce <= 0:
                return "Friction"
            else:
            #Otherwise calculates the acceleration of the object based on newtons second law F = m * a and after that returns True
                app.acceleration  = self.netforce/self.mass
                return True

#The Class where the graphics as in the triangle and the blocks movement are simulated and created
class Graphics:
    def __init__(self, degree):
        #Initialisation of the different values that we get in input
        self.degree = degree #Inputed Angle
    
    #Method that creates the "wall" that object hits, since it seemed as a simple and "fun" way of stopping the object    
    def ObjectWall(self):
        self.wall = Rect(0, 0, 10, 400, fill="brown")
    
    #Method that creates the inclined plane as in the triangle automatically based on the degrees that were inputed by the used    
    def Triangle(self):
        #Converts the degrees into radians in order to calculate the triangle angle and size, shape and etc
        triangle_degree = m.radians(self.degree)
        
        #The base coordinates that we have predetermined 
        x1, y1 = 10, 400
        x2, y2,= 400, 400
        
        #Calculates the base of the triangle based on the distance from x1,y1 to x2,y3
        base = distance(x1, y1, x2, y2)
        #Calculates the height of the triangle based on property that the base which is the adjacent side multiplied with tan(degree) of the triangle
        height = abs(rounded(base * m.tan(triangle_degree)))
        #Calculates the third and final points of x3 and y3; y3 being the windows y_max - height
        self.x3, self.y3 = 400, y2 - height
        #Creates and forms the triangle as a polygon with three points
        self.ramp = Polygon(x1, y1, x2, y2, self.x3, self.y3, fill="dodgerBlue")
        
    #Method that creates the object thats in movement
    def ObjectBlock(self):
        #Sets the height of the object based on degree due to an aesthetic reason
        object_height = self.degree 
        #Sets the base of the object based on some math, but has no major reason but looke good thats why
        object_base = rounded(object_height/ m.tan(m.radians(self.degree)))
        #I applied the same principle with the object here as i did with the triangles
        #In essence by calculating the other points based on coordinates
        #Could've should've done with Rect instead but wanted to challenge myself slightly
        x_coord, y_coord = self.x3, self.y3 
        x2, y2 = (x_coord), (y_coord + object_height)
        x3, y3 = (x_coord - object_base), (y_coord + object_height)
        x4, y4 = (x_coord - object_base), (y_coord)
        
        #Calculates how much should i rotate the figure so it seams that it is descending the inclined plane
        slope = 90 - self.degree
        #Creates the block
        self.block = Polygon(x_coord, y_coord, x2, y2, x3, y3, x4, y4, rotateAngle = slope, fill = gradient("red", "black", start = "top"))
        #Sets the block to back so it seams more fluid graphically speaking
        self.block.toBack()
        
    #Method that Shows a screen that invalid values have been shown and the option to exit the application
    def InvalidScreen(self):
        app.background = "black"
        self.L1 = Label("Invalid Mass or Angle was entered", 200, 200, fill="white")
        self.L2 = Label("Press 'E' to Exit Application", 200, 250, fill="white")

#Function that uses keybind e to exit the application            
def onKeyPress(key):
    if key == "e":
        print("Application Terminated")
        app.stop()

#Inbuilt methods/functions that allow you to get a pop up to ask for user input on mass, angle, frictioncoeffecient
mass = float(app.getTextInput("Enter A Valid Mass (Anything above 0)"))
angle = float(app.getTextInput("Enter A Valid Angle on the Triangle (Anything between 0 and 45)"))
frictioncoeffecient = float(app.getTextInput("Enter the Friction-Coeffecient (Recommended frictions-coeffecient intervall 0 to 1)"))

#Labels/signs showing the time and velocity the object takes and has
l = Label(app.time, 200, 15, fill="red")
l2 = Label(app.velocity, 200, 30, fill="red")

physics = Physics(mass, angle, frictioncoeffecient)
graphics = Graphics(angle)

#Different checks to run the program based on the force method 
if physics.Force() == True:
    #Creates graphically the triangle, wall and object 
    graphics.Triangle()
    graphics.ObjectWall()
    graphics.ObjectBlock()
    
    #Runs the following code automatically in the "shadows" or behind
    def onStep():
        #Functions in essence as a while loop; loops the code till the condition is fullfilled; being that till the object hits the wall
        if graphics.block.hitsShape(graphics.wall) == False:
            app.time += (1/app.stepsPerSecond) #How quickly the time is incremented
            app.velocity += (app.acceleration * (1/app.stepsPerSecond)) #Calculates how velocity is changing
            l.value = app.time #Updates the labels values to represent the time
            l2.value = app.velocity #Updates the labels values to represent the velocity
            
            #Using some cool math and physics to change and update the position of the blocks center x and y based on the distance the object travels and ...
            #This based on the distance formula in physics but I use cos and sin to adjust the distance so it follows the curvuture of the inclined plane
            graphics.block.centerX -= ((app.acceleration * (app.time**2))/2)*m.cos(m.radians(graphics.degree))
            graphics.block.centerY += ((app.acceleration * (app.time**2))/2)*m.sin(m.radians(graphics.degree))
        else:
            #After the "while loop" is fullfilled it shows the "endscreen" where the following data is represented
            print(distance(10, 400, graphics.x3, graphics.y3))
            background_screen = Rect(0, 0, 400, 400)
            average_velocity = distance(10, 400, graphics.x3, graphics.y3)/app.time
            l.toFront()
            l2.toFront()
            l.value = (app.time, "seconds (The time it the object to travel)") 
            l2.value = (average_velocity, "units per second (Average Velocity)")
            app.stop()
            
#Different checks to run the program based on the force method 
elif physics.Force() == False:
    l.fill = "black"
    l2.fill = "black"
    graphics.InvalidScreen()
    
#Different checks to run the program based on the force method     
elif physics.Force() == "Friction":
    l.fill = "white"
    l2.fill = "white"
    Label("Friction is way too large, hence the object is still", 200, 200, fill="black")
    app.stop()

#Tids felmarginal ungefär 10 till 12% mindre än de borde --> alltså det bli fel på ungefär 10% så om det står 1.5s det borde var 1.66s 
#Men detta felmarginal beräkning kan vara fel eftersom, jag använder ett tidtagaur för att mäta data som gör att mätningsfel kan ske 
#Troligtvis orsaken till varför det är ett sån felmarginal är på grund av att jag anta att sträckan och objektets centerkoordinater är i samma led
#Detta kan gör att distans objektet behöver faktiskt åka är inte helt rätt
## Mission 0: Rough Seas and Enter the Pacific
### Images from Robosub Mission Overview
![[Screenshot 2024-06-11 at 1.41.02 PM.png]]![[Screenshot 2024-06-11 at 1.41.55 PM.png]]
### Steps to Complete
1. The sub must start next to the dock in either the tails or heads position depending on a coin flip done at the side of the pool. 
2. After starting the sub will start scanning for the gate using the [[Neural Network#Object Detection Algorithm 1|Object Detection Algorithm #1]]. 
3. After the gate has been detected, the sub must travel to the gate using the movement package. 
4. After arriving at the gate, the [[Neural Network#Object Detection Algorithm #2|Object Detection Algorithm #2]] is triggered to detect which side of the gate has the correct arrow. 
5. After the side of the gate has been identified, the sub will travel through that side using the movement package.
6. After traveling through the gate, the sub will complete three complete rotations around the yaw direction. 
7. Then the sub will end with an idle state while the state machine is switched to the next state.
### Graphic Overview
![[Screenshot 2024-06-12 at 1.00.57 PM.png]]
## Mission 1: Path Finding x 2
### Images from Robosub Mission Overview
![[Screenshot 2024-06-12 at 1.03.20 PM.png]]
### Steps to Complete
1. The sub starts in the Idle state after completing the first mission.
2. The sub moves using the Movement Package while using the [[Neural Network#Object Detection Algorithm #3|Object Detection Algorithm #3]]. 
3. When the third object detection algorithm detects the start of the path, the sub travels along the path outlined using the Movement Package again.
4. After completing the path outlined, the sub returns to the idle state
### Graphic Overview
![[Screenshot 2024-06-12 at 2.13.27 PM.png]]
## Mission 2: Hydrothermal Vent | Buoy
### Images from Robosub Mission Overview
![[Screenshot 2024-06-12 at 1.07.56 PM.png]]
### Steps to Complete
1. Starting in Idle position, start moving forward.
2. Keep moving forward until the [[Neural Network#Object Detection Algorithm #1|Object Detection Algorithm #1]] detects the Red Buoy. 
3. After the Red Buoy has been detected, keep moving towards the buoy until the arm touches the buoy. 
4. After the arm touches the buoy, rotate in the predefined direction depending on the gate side. 
5. After completion go around the buoy on the right side and move beyond the task. 
6. After moving past the buoy, the sub returns to the Idle state.
### Graphic Overview
![[Screenshot 2024-06-12 at 3.40.46 PM.png]]
## Mission 3: Ocean Temperatures | Bins
### Images from Robosub Mission Overview
![[Screenshot 2024-06-12 at 1.10.02 PM.png]]
### Steps to Complete
1. Starting in the Idle state, transition into a scanning state to locate the marker using the [[Neural Network#Object Detection Algorithm #1|Object Detection Algorithm #1]].
2. After locating the marker, move closer to the marker and position the claw around the marker.
3. Close the claw and carry the the marker to the Bin.
4. While over the bin, identify the correct side of the bin dependent on the gate side using the [[Neural Network#Object Detection Algorithm #4|Object Detection Algorithm #4]]. 
5. Place the marker in the correct side of the bin. 
6. Travel away from the bin and go to the Idle state.
### Graphic Overview
![[Screenshot 2024-06-12 at 7.18.00 PM.png]]
## Mission 4: Mapping | Torpedoes
### Images from Robosub Mission Overview
![[Screenshot 2024-06-12 at 7.21.09 PM.png]]
### Steps to Complete
1. Starting in the idle position, start scanning for the mission using the [[Neural Network#Object Detection Algorithm #1|Object Detection Algorithm #1]]
2. Using the movement package, pilot the sub to within one meter of the prop. 
3. After arriving within one meter of the mission, the [[Neural Network#Object Detection Algorithm #5|Object Detection Algorithm #5]] is triggered to locate the smallest octagon and second smallest octagon.
4. After the smallest and second smallest octagons are located. The sub is piloted to be in front of the smallest octagon and a torpedo is fired.
5. After the first torpedo is fired, the sub is piloted to be in front of the second smallest octagon and the second torpedo is fired. 
6. After the second torpedo is fired, the sub is piloted around the prop and positioned behind it.
7. The sub returns to the Idle state. 
### Graphic Overview

## Mission 5: Collect Samples | Octagon
### Images from Robosub Mission Overview
![[Screenshot 2024-06-12 at 7.23.36 PM.png]]
![[Screenshot 2024-06-12 at 7.23.53 PM.png]]
### Steps to Complete
1. Starting in the Idle State, using the [[Neural Network#Object Detection Algorithm #1|Object Detection Algorithm #1]] to identify the location of the prop.
2. After locating the prop, switch states to the Movement Package, moving towards to the prop.
3. After arriving at the prop, decrease height to go under the octagon.
4. Using the [[Neural Network#Object Detection Algorithm #6|Object Detection Algorithm #6]] to identify the props that need to be moved.
5. After identification, switch to the movement package and move closer to the props.
6. Position the claw around the props and switch to the grab state.
7. After the prop is grabbed, using the movement package position the prop over the collection basket.
8. After the prop is over the collection basket, switch to the release state. 
9. Go back to step 5 and repeat until all props are in the collection basket.
10. After all props are moved, switch to the movement package and move past the prop.
11. After completion switch back to the Idle state. 
### Graphic Overview



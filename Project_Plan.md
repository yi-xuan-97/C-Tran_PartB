#Project Plan
Our project objective will be to analysis C-Tran bread crumb data. There are three team working on this project and our team will be working on Part-B which is to characterize the deviation of the GPS location record of the bus. This means that we need to find out which direction the deviation is pointing to and visualization it.

For bread crumb data, there could be many reason that lead to it. For example, it could be the cause of driver, error in trip plan, error in GPS sensor, GPS sensor bias and so on. As for our job, we basically divided into three part. First of all, we need to use statistic to show a basic description of the data and then visualize them. To reach this goal, we will use pandas library and matlibplot birary (or Seaborn library) as our basic tools to reach our goal. Secondly, we need to find out which direction the deviation happened, which will be a number from 0 to 360 indicating an angle. Our idea of approach this goal is that we treat the actual recorded point and the standard point as two point and we use find the azimuth angle of them.

After getting deviation, we will operate and analyze this data. We can calculate the trip deviation from the individual reading deviations by those methods: Sum all breadcrumb reading deviations over the trip, Sum the squares of all breadcrumb deviations over the trip,Maximum breadcrumb deviation for a trip and so on. After finding the most suitable method, statistics and visualization can be performed based on “trip deviation.” After getting the data table based on "trip deviation", we are equivalent to having a basic data set. So we can build a machine learning model on this data set. Use several weeks of data as a training set for supervised learning training.


Our team structure will be a division of labor to complete the required work. We will look for related papers together as a reference. Importing data and visualizing the data are temporarily determined to be yixuan's work.Analyze all data and draw conclusions are temporarily decided to work for tianhui. We will complete the research paper together.

Five Milestone:
Use statistic get the output of the basic description
Use tools to visualized the output
Get the deviation direction
Analysis the deviation
Analysis total result

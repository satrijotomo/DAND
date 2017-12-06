
### Summary

This interactive and animated visualization shows a number of summary statistics based on the individual baseball players. 
The animated charts would give readers insights into the correlation between the player's height, handedness and home run. Some of them are listed below.

1. The players height distribution chart shows normal curve pattern as expected, with majority of players' heights are in the range of 72-73 inches. This is the same for all handedness group.
2. Interestingly, the maximum home run of each height group also follows similar pattern, albeit less consistent. Only in Right handedness group that the highest maximum value falls within 74-75 inches; for the other two handedness groups it falls in 72-73 inches.
3. Across the handedness groups, the highest home run recorded is 548. This record is of a right-handed player within height range 74-75 inches. However, his performance is an outlier since average home run of his group is only 55.
3. In general, average home run value in each group is not more than 100.

### Design

The most important decision is what information to present in the chart. First I chose bubble chart (Project6Baseball4.htm and earlier versions), however I found that this type of chart alone was not the best option in communicating my data. I then decided to use bar chart and bubble chart with height as X-axis and two Y-axis: count of players and home run. 
Then I used handedness as the filter of data for animation. The next decision was to choose between D3 JS or Dimple JS. I chose Dimple JS with storyboard based on its simpler way of building the animated and interactive chart. Furthermore, there are multiple advance Dimplejs examples available at http://dimplejs.org/. 

I don't consider removing outliers in the data since the dataset is curated one and I believe I need to present all of the in the chart. With that being said, I removed one duplicated row with the same name and other matrics from the dataset and couple of columns as explained in the Fix section.

### Feedback

Feedback received for Project6Baseball3.html:

1. On the "L" handedness frame, there is bubble that crossed the top line of the chart. While this is not a blocking issue, it is better that all bubbles are within the chart's boundaries.

2. Legend on the right side of the animation is not pleasing to the eyes. The text is not alligned with the chart height and seems out of place.

3. Color used in the chart's bubbles overlap with the colors used in legend, but they convey different messages. This causes confusion for the readers.


Feedback received for Project6Baseball4.html:

1. Explore other chart type to effectively communicate the message
2. Select either height or weight and group the values in bins

### Fix

Based on feedback for Project6Baseball3.html, I implemented changes for Project6Baseball4.html:
1. Add parameter for maximum X and Y axis values to avoid bubbles overreach
2. Change the default and indicator colors of right hand legend. I use default dimple JS colors which are not use in the animation. The choices of colors are limited in dimple JS default color, but now the color distinction between animation and legend are clear.
3. Lower the legend section on the right side and increase the text a little bit for readability
4. Add google font to make the title and legend text more pleasing to the eyes and not standard html font
5. Add bootstrap navbar to add more aesthetic

Based on feedback for Project6Baseball4.html, I implemented changes for Project6Baseball5.html:
1. Edit the csv data file to add heightGroup and Count columns
2. Use bar chart for players count and bubble chart for maximum, average and minimum home run values
3. Adjust position of the legend

### Resources

I use mainly two resources:
1. Example codes in Data Visualization course
2. Advance examples with storyboard in Dimplejs.org
3. Wiki github of dimplejs https://github.com/PMSI-AlignAlytics/dimple/wiki/ to understand options and parameters.

As usual, I also use stackoverflow to find solutions for the issues that I face.





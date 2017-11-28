
### Summary

This interactive and animated visualization shows a number of summary statistics based on the individual baseball players. The graph shows that in total more home runs created by right handed players. It also shows that there is no obvious correlation between players' weight and height and home runs. (edit: Change the summary)

### Design

The most important decision is what information to present in the chart. I decided to use height as X-axis, weight as Y-Axis and homerun as Z-axis. Then I used handedness as the filter of data for animation. The next decision was to choose between D3 JS or Dimple JS. I chose Dimple JS with storyboard animation based on the ease of building the chart and that there are multiple advance examples available in http://dimplejs.org/. 

For the readers to compare the chart between handedness, I override the minimum and maximum X and Y axis values. This change makes the chart axis values do not change from one frame to another. 

I don't consider removing outliers in the data since the dataset is curated one and I believe I need to present all of the in the chart. With that being said, I removed one duplicated row with the same name and other matrics from the dataset.

### Feedback

After presenting the chart (Project6Baseball3.html), I received some feedbacks. The feedbacks can be summarized as follow
Input:

1. On the "L" handedness frame, there is bubble that crossed the top line of the chart. While this is not a blocking issue, it is better that all bubbles are within the chart's boundaries.

2. Legend on the right side of the animation is not pleasing to the eyes. The text is not alligned with the chart height and seems out of place.

3. Color used in the chart's bubbles overlap with the colors used in legend, but they convey different messages. This causes confusion for the readers.


### Fix

Based on the above feedback, I created next iteration of the visualization, Project6Baseball4.html. The changes in this version are:
1. Add parameter for maximum X and Y axis values to avoid bubbles overreach
2. Change the default and indicator colors of right hand legend. I use default dimple JS colors which are not use in the animation. The choices of colors are limited in dimple JS default color, but now the color distinction between animation and legend are clear.
3. Lowered legend on the right side and increase the text a little bit for readibility.
4. Add google font to make the title and legend text more pleasing to the eyes and not standard html font.
5. Add bootstrap navbar to add more aesthetic

### Resources

I use mainly two resources:
1. Example codes in Data Visualization course
2. Advance examples with storyboard in Dimplejs.org
3. Wiki github of dimplejs https://github.com/PMSI-AlignAlytics/dimple/wiki/ to understand options and parameters.

As usual, I also use stackoverflow to find solutions for the issues that I face.





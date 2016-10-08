# Comma separated values go in this XLS file:
output = open('Output.csv', 'w');

# This is the label we're looking for:
lookFor = 'category key="';
upTo = '"';

# Helper variables:
offset = len(lookFor);
previousLevel = 0;
parents = [];

# Read the XML file line by line:
with open('Full Data Model.xml', 'r') as input:
	for line in input:
		index = line.find(lookFor);
		# If it's an interesting line (e.g. one that contains the label we're looking for):
		if index != -1:
			# Find the nesting level of that line (by counting its leading spaces):
			spacesUpTo = line.find('<');
			level = spacesUpTo/4 - 1;
			upToIndex = line[index+offset:].find(upTo);
			# Extract the keyword the label defines:
			leaf = line[index+offset:index+offset+upToIndex];
			print leaf, level, previousLevel
			print 'Before: ', parents
			# Keep track of the current nesting chain:
			if (level == previousLevel + 1):
				# print 'ADDING '+ leaf
				parents.append(leaf);
			if (level == previousLevel):
				# print 'CHANGING '+ parents[-1] + ' TO ' + leaf
				parents[len(parents)-1] = leaf
			if (level == previousLevel - 1):
				print 'DELETING '+ parents[-1]
				del parents[len(parents)-1];
				parents[len(parents)-1] = leaf
			print 'After: ', parents
			print ' '
			previousLevel = level;
			# Write the keyword to the output file with the correct chain of parents:
			for parent in parents:
				output.write(parent);
				output.write('.');
			output.write(', (please fill this cell manually)\n');

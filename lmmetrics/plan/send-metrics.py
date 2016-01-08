import os.path
import datetime
# print dir()
# print vars()
# print dir(context)

#create metrics dictionary
metrics = {}

#need to find the ID number of the individual deployment:
task = context.task
real_task = taskBlockService.getTask(task.id)

print real_task.steps

print real_task  #echoes this out on the UI for visibility
#print task.metadata['application']
#print task.metadata['version']
#print task.metadata['taskType']
#print real_task.startDate
#print real_task.completionDate
#print real_task.failureCount
#print real_task.id
#print real_task.state


#populate dictionary with metric data
metrics['application'] = task.metadata['application']
metrics['environment'] = task.metadata['environment_id']
metrics['version']     = task.metadata['version']
metrics['taskType']    = task.metadata['taskType']
metrics['startDate']   = real_task.startDate
metrics['completionDate'] = real_task.completionDate
metrics['errorCode']      = real_task.failureCount
metrics['id']		= real_task.id
metrics['deployed'] = real_task.state

print "DICT: ", metrics

doneTime = metrics['completionDate']
if doneTime is None:
    #print "Nothing"
    doneTime = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%fZ')
    print "NOW: ", datetime.datetime.utcnow()
    print doneTime

#print doneTime

#echo this stuff out to the UI
#for k,v in metrics.items():
#    print k
#    print v

#breaking the environment apart by the / as delimeter.
env2 = [substring.strip() for substring in metrics['environment'].split('/')]  #  output results in this:    ['Environments', 'Distribution', 'PASVCQBE', 'test-b', 'PASVCQBE_test-b']
#pick out a couple key components (prob not needed to set these to new vars) targetApp = env2[2] targetEnv = env2[3]

#print out some stuff, can remove these print statements later in life if desired print 'env2 is ' + str(env2) print 'targetApp is ' + targetApp + ' and targetEnv is ' + targetEnv

# location to save log files
save_path = 'log/deploymetrics/'

#create folders to organize logs if they don't exist
if not os.path.exists(save_path):
    print save_path, "Metrics folder does not exist creating new folder for metrics!"
    os.makedirs(save_path)

#name the file we will ultimately write to home slice:
logFileName = str(task.metadata['application']) + '.' + str(metrics['id']) + '.deployMetrics.csv'
fullLog = save_path + logFileName

#now print out some data about it, which of course can be removed later as needed print 'logFileName is set to ' + logFileName print 'logFileName type is:'
print type(save_path)
print type(logFileName)

#deal with date strings
startDateRaw = metrics['startDate']

#remove these later
print 'startDateRaw is set to ' + str(startDateRaw)

dateString = str(startDateRaw)

#pull date strings apart
startDateDict = [substring.strip() for substring in dateString.split('T')]
startDate = startDateDict[0]
startTimeRaw =  [substring.strip() for substring in startDate[1].split('Z')]

#resulting in time of startTimeRaw[0]
print 'startDateDict is set to ' + str(startDateDict)
print 'startDate is set to ' + str(startDate)
print 'startTimeRaw is set to ' + str(startTimeRaw)

#concat the data into a csv string which we will later write to a file #data will feed these links:
#       http://deploystatus-pm/dep_logs_data/  #  http://picollaboration.lmig.com/Sites/ATSDeployServices/DARTS%20FlightBoard/BFDevStat.mht
#
#       To be arranged as such in the flat file:
#               Date, Start Time, Stop Time, Environment, Domain, AppAlias, EarName, returnCode, Build, Duration of Deploy
#

csvdata = str(metrics['startDate']) + "," + str(doneTime) + "," + str(metrics['environment']) + "," + str(metrics['application']) + "," + str(metrics['errorCode']) + "," + str(metrics['version']) + "," + str(metrics['deployed'])

# Write to a file:
logfile = open(fullLog, 'w')
logfile.write (str(csvdata))
logfile.close()
print fullLog + " Has been created to record the metrics for this deployment!"
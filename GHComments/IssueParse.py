from githubutils import GitHub
import json
import csv
import pandas


projects = pandas.read_csv('apacheGhProjects2.csv', index_col = False )
projList = list(projects.projects)

print("Here starts everything")

gh = GitHub("SoutiRini", "xxxx")

print("connected to github")

for project in projList:

    repo_call = "/repos/apache/" + str(project) + "/issues"
    Issues = gh.doApiCall(repo_call, params={'state': 'all'})

    print("fetching issues for project" + str(project))

    # print(Issues)
    if (Issues == None ):
        print("something wrong with: "+ project)


    IssueNumbers = [issue['number'] for issue in Issues]

    IssueTitles = [issue['title'] for issue in Issues]

    IssueBodies = [issue['body'] for issue in Issues]

    issue_filename = "issues_" + str(project) + ".json"

    with open(issue_filename, 'w') as f:
        json.dump(Issues, f)

    # Issues = json.load(open('issues.json'))



    Comments = []

    print("starting to fetch comments for " + str(project))

    for issue in Issues:
        commentCall = ("/repos/apache/" + str(project)+ "/issues/" + str(issue['number']) + "/comments");
        IssueComments = gh.doApiCall(commentCall)
        Comments.append([comment['body'] for comment in IssueComments])

    comment_filename = "comments_" + str(project) + ".json"
    with open('comment_filename', 'w') as f:
        json.dump(IssueComments, f)

    # Comments = json.load(open('comments.json'))



    data = zip(IssueNumbers, IssueTitles, IssueBodies, Comments)

    data_list = list(data)

    data_list.insert(0, ('IssueNumbers', 'IssueTitles', 'IssueBodies', 'Comments'))

    parsed_filename = str(project)+".csv"

    with open(parsed_filename, 'w') as f:
        wr = csv.writer(f, quoting=csv.QUOTE_ALL)
        wr.writerows(data_list)



print("End of projects")

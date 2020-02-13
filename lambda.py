import json

def lambda_handler(event, context):
    #获取group信息
    groups= event['authorizationToken'].split(",")
    
    allow_response = {
          "principalId": "random",
          "policyDocument": {
            "Version": "2012-10-17",
            "Statement": [
              {
                "Action": "execute-api:Invoke",
                "Effect": "Allow",
                "Resource":"arn:aws:execute-api:ap-northeast-1:764444585758:6zpmmv174e/*/GET/"
              }
            ]
          },
          #需要传递给后端lambda的值
          "context": {
            "key": "value",
            "numKey": 1
          }
        }

    deny_response= {
      "principalId": event['authorizationToken'],
      "policyDocument": {
        "Version": "2012-10-17",
        "Statement": [
          {
            "Action": "execute-api:Invoke",
            "Effect": "deny",
            "Resource":"arn:aws:execute-api:ap-northeast-1:764444585758:6zpmmv174e/*/GET/"
          }
        ]
      }
    }
    #如果只属于一个group，且为本组，则允许访问
    if (len(groups) ==1):
      if (event['authorizationToken'] == 'group1'):
        response = allow_response

      #否则deny
      else:
        response = deny_response
      return response
    else:
      #如果有多个group信息，只要有一组是本组资源，允许访问；
      for group in groups:
        #print(group)
        if (group == 'group1'):
          response = allow_response
          return response
      
      #循环完毕，没有本组信息，deny
      response = deny_response          
      return response
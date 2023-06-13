import asyncio
import pymsteams

team_message = pymsteams.connectorcard("https://sophosbanking.webhook.office.com/webhookb2/3f049424-39a1-4899-afda-52ec3e1ec97a@0cf11b83-d338-43a4-ba90-34cfa9985885/IncomingWebhook/9e077b6514884b6ea09ee63df024b162/09e86cd8-bb3f-4233-8905-ca406f4973d0")

potential_action_1 = pymsteams.potentialaction(_name = "Approve or Reject")
# You can add a TextInput to your potential action like below - Please note the 2nd argument below as the id name
potential_action_1.addInput("TextInput","comment","Approve or Reject",False)
# we use the 2nd argument above as the id name to parse the values into the body post like below.
potential_action_1.addAction("HttpPost","Add Comment","https://7xnxc3coapmzuol46x7wbwghd40tmmyy.lambda-url.us-east-2.on.aws/", "{{comment.value}}")


potential_action_3 = pymsteams.potentialaction(_name = "Change Status")
potential_action_3.choices.addChoices("Approve","0")
potential_action_3.choices.addChoices("Reject","1")
potential_action_3.addInput("MultichoiceInput","list","Select a status",False)
potential_action_3.addAction("HttpPost","Save","https://7xnxc3coapmzuol46x7wbwghd40tmmyy.lambda-url.us-east-2.on.aws/",)

team_message.addPotentialAction(potential_action_1)
team_message.addPotentialAction(potential_action_3)

team_message.title("Manual Approval")
team_message.color("7b9683")

# Add text to the message.
team_message.text("Approve or deny deployment")
team_message.summary("Approval deployment")

team_message.send()

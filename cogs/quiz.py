from random import randint
from weakref import WeakValueDictionary

QuizData = {
    "kanji":(
        ("日","hi","ひ","bi","び","nichi","にち"),
        ("本","hon","ほん"),
        ("一","ichi","いち"),
        ("二","ni"",に"),
        ("三","san","さん"),
        ("四","shi","し","yon","よん","yo","よ"),
        ("五","go","ご"),
        ("六","roku","ろく"),
        ("七","shichi","しち","nana","なな"),
        ("八","hachi","はち"),
        ("九","kyuu","きゅう","ku","く"),
        ("十","jyuu","じゅう"),
        ("語","go","ご"),
        ("何","nani","なに","nan","なん"),
        ("月","getsu","げつ","gatsu","がつ","tsuki","つき"),
        ("火","ka","か"),
        ("水","sui","すい","mizu","みず"),
        ("木","moku","もく","ki","き"),
        ("金","kin","きん","kane","かね"),
        ("土","do","ど"),
        ("人","hito","ひと","jin","じん","nin","にん"),
        ("時","ji","じ","toki","とき"),
        ("分","fun","ふん","pun","ぷん"),
        ("半","han","はん"),
        ("年","nen","ねん","toshi","とし"),
        ("小","chii","ちい","shou","しょう"),
        ("学","gaku","がく"),
        ("校","kou","こう"),
        ("生","sei","せい"),
        ("中","chuu","ちゅう","naka","なか"),
        ("今","ima","いま","kon","こん"),
        ("才","sai","さい"),
        ("行","i","い"),
        ("上","ue","うえ"),
        ("下","shita","した"),
        ("右","migi","みぎ"),
        ("左","hidari","ひだり"),
        ("名","na","な"),
        ("前","mae","まえ"),
        ("円","en","えん"),
        ("男","otoko","おとこ"),
        ("女","onna","おんな"),
        ("子","ko","こ"),
        ("大","dai","だい","tai","たい","oo","おお"),
        ("先","sen","せん"),
        ("目","me","め"),
        ("口","kuchi","くち"),
        ("手","te","て"),
        ("出","de","で"),
        ("入","hai","はい","i","い"),
        ("私","watashi","わたし")
    )
}

ongoingQuiz = WeakValueDictionary()

async def quizStart(client, message):
    output = ""
    if message.channel.id not in ongoingQuiz:
        term = message.content.lower().replace("!quiz start ", "")
        if term != "":
            if term in QuizData:
                newQuiz = Quiz()
                ongoingQuiz[message.channel.id] = newQuiz
                await newQuiz.setup(client, message, term)
            else:
                output = "Not a valid quiz name"
        else:
            output = "Please enter a quiz name"
    else:
        output = "A quiz is currently going!"
    if output != "":
        await client.send_message(message.channel, output)

async def quizStop(client, message):
    if message.channel.id in ongoingQuiz:
        await ongoingQuiz[message.channel.id].finish()
    else:
        await client.send_message(message.channel, "No quiz is currently going")

async def quizList(client, message):
    output = "List of all quiz names:\n```\n"
    names = list(QuizData.keys())
    if len(names) > 1:
        for i in range(0, len(names)-1):
            output += "- {0}\n".format(names[i])
    else:
        output += "- {0}".format(names[0])
    output += "```\n"
    output += "To start a quiz the command is:\n```\n!quiz start [name]\n```"
    await client.send_message(message.channel, output)

class Quiz:
    async def setup(self, client, message, term):
        self.client = client
        self.channel = message.channel
        self.stop = False
        self.used = []
        self.won = False
        self.score = {}
        self.items = QuizData[term]
        self.winner = "None"
        await self.start(term)

    async def start(self, term):
        await self.client.send_message(self.channel, "The {0} quiz has started\nThe first player to get to 10 points, wins!\n(20 second timeout)".format(term))
        await self.run()

    async def finish(self):
        self.stop = True
        await self.client.send_message(self.channel, "The quiz has stopped!")
        if len(list(self.score.values())) != 0:
            await self.printScoreScreen()
        await self.end()

    async def draw(self):
        await self.client.send_message(self.channel, "I've run out of questions! - It's a Draw!")
        await self.printScoreScreen()
        await self.end()

    async def run(self):
        count = 0
        while (not self.won) and (not self.stop):
            if len(self.items) > len(self.used):
                count += 1
                num = randint(0, len(self.items)-1)
                while num in self.used:
                    num = randint(0,len(self.items)-1)
                self.currentQ = self.items[num]
                self.question = self.currentQ[0]
                self.used.append(num)
                await self.ask(count)
            else:
                await self.draw()
                break


    async def ask(self, counter):
        await self.client.send_message(self.channel, "Question "+str(counter)+":\n"+self.question)
        resp = await self.client.wait_for_message(timeout=20, channel=self.channel, check=self.check)
        if not self.stop:
            output = ""
            if resp is None:
                output = "The answer was: "+" ".join(self.currentQ[1:(len(self.currentQ)-1)])
            else:
                if resp.author.id in self.score:
                    self.score[resp.author.id] += 1
                    if self.score[resp.author.id] == 10:
                        await self.gameOver(resp.author)
                    else:
                        output = resp.author.mention + " Correct! +1 for you!"
                else:
                    self.score[resp.author.id] = 1
                    output = resp.author.mention + " Correct! +1 for you!"
            if output != "":
                await self.client.send_message(self.channel, output)

    async def gameOver(self, winner):
        self.won = True
        self.winner = winner
        await self.printScoreScreen()
        await self.end()

    def check(self, msg):
        x = False
        for i in range(1,len(self.currentQ)-1):
            if self.currentQ[i] == msg.content.lower():
                x = True
                break
        return x

    async def printScoreScreen(self):
        output = ""
        if self.winner != "None":
            output = "Winner: {0}!\n".format(self.winner.mention)
        users = list(self.score.keys())
        scores = list(self.score.values())
        output += "```\n"
        if len(users) > 1:
            unOrdered = True
            while unOrdered:
                unOrdered = False
                for i in range(0,len(users)-2):
                    if scores[i] > scores[i+1]:
                        scores[i+1],scores[i] = scores[i],scores[i+1]
                        users[i+1],users[i] = users[i],users[i+1]
                        unOrdered = True
            for i in range(0,len(users)):
                user = await self.client.get_user_info(users[i])
                mentionName = user.display_name
                output += str(scores[i]).ljust(3," ") + ": "
                output += mentionName
                output += "\n"
        else:
            user = await self.client.get_user_info(users[0])
            mentionName = user.display_name
            output += str(scores[0]).ljust(3," ") + ": " + mentionName + "\n"
        output += "```"
        await self.client.send_message(self.channel, output)

    async def end(self):
        del ongoingQuiz[self.channel.id]

from openai import OpenAI
import concurrent.futures
import sys

sys.path.append("..")
import fixedSentences
from Components import slotFiller4pre
from Components import imageGenerator
from Components import paraphraser
from Components import slotFiller4FB
from Components import upgradeprereco
from Components import upgradeprerect
from Components import entityExtractor
from Components import upgradeSlotFiller
from DAO import dbops
import json


# uid = "asdkhasd"

def postrec_interface(round, uid):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        aftfix = ''
        if round == 'one':
            #upgradeSlotFiller.profile_editor(uid=uid)
            slotFiller4pre.profile_editor(uid=uid)
            prefix = fixedSentences.prefixes["rec"]
            aftfix = fixedSentences.prefixes["aftrec1"]
            lst1 = executor.submit(upgradeprereco.prereco_interface, uid)
            lst2 = executor.submit(upgradeprerect.prerect_interface, uid)
            lst1res = lst1.result()
            lst2res = lst2.result()
            # lst1 = prereco.prereco_interface()
            # lst2 = prerect.prerect_interface()
            lst = lst1res + lst2res
        if round == 'two':
            dbops.upaccfrst(uid, 'False')
            # slotFiller4FB.profile_editor()
            prefix = fixedSentences.prefixes["recfb"]
            aftfix = fixedSentences.prefixes["aftrec2"]
            lst1 = executor.submit(upgradeprereco.prereco_interface, uid)
            lst2 = executor.submit(upgradeprerect.prerect_interface, uid)
            lst1res = lst1.result()
            lst2res = lst2.result()
            # lst1 = prereco.prereco_interface()
            # lst2 = prerect.prerect_interface()
            lst = lst1res + lst2res

        goal = dbops.getgoal(uid)
        emo = dbops.getemo(uid)
        eh = dbops.geteh(uid)
        limit = dbops.getlimit(uid)
        fb = dbops.getlastusersent(uid).replace("user:", "")
        prefood = dbops.getpreferencefood(uid)
        preflavor = dbops.getflavorpreference(uid)
        LTMinfo = dbops.getLTM(uid)
        exercise = dbops.getexercise(uid)
        con = dbops.getcon(uid)
            
        if LTMinfo == '':
            LTMinfo = 'none'
        
        f1 = lst[0]
        f2 = lst[1]
        f3 = lst[2]
        f4 = lst[3]
        f5 = lst[4]
        f6 = lst[5]
        f7 = lst[6]
        f8 = lst[7]
        f9 = lst[8]
        f10 = lst[9]

        recPrompt = '''
        *Your information:
        [emotion status] -> <{emotion}>
        [eating habit] -> <{eatinghabit}>
        [dining time limitation] -> <{limitation}>
        [dietary goal] -> <{eatinggoal}>
        [exercise frequency] -> <{exercise}>
        [dietary restriction] -> <{con}>
        [feedback] -> <{feedback}>
        [food preference] -> <{preferedfood}>
        [flavor preference] -> <{preflavor}>
        [additional conditions] -> <{LTMinfo}>
        [food list one] -> <{food1}>,<{food2}>,<{food3}>,<{food4}>,<{food5}>
        [food list two] -> <{food6}>,<{food7}>,<{food8}>,<{food9}>,<{food10}>
    
        *Requirements:
        1. The foods I recommend MUST be *nutritionally balanced* and *varied*, including *carbs*, *vitamins*, and *protein*.
        2. If your [emotion status] is <negative>, I will recommend comfort food, with a warm, soft, sweet taste.
        3. If your [eating habit] is <causal>, I will assume you are hungry, and recommend more carb-heavy, satiating foods.
        4. If your [dining time limitation] is <sufficient>, I will recommend sumptuous cuisine; if your [time limitation] is <limited>, I will recommend very common and easy to prepared foods, such as fast foods.
        5. If your [food preference] and [flavor preference] are not 'none', I will try to recommend a food according to them.
        6. I will recommend food that is beneficial for your [dietary goal] and incorporate the reason into <reason>.
        7. If your [exercise frequency] is <frequent>, I will recommend a food that is beneficial for boosting and recuperating energy.
        8. I will carefully consider the [feedback] before making recommendations. If your [feedback] is not healthy, I would not adopt it and I would state this in my explanation and recommend a good healthy diet.
        9. I will not recommend food conflicting to your [dietary restriction].
        10. [additional conditions] may include your resource constraints, religous belief, and special health conditions. If [additional conditions] is not 'none', I will consider these aspects when selecting food and incorporate these part of information in explanation.
        11. I must make sure the two foods I recommend distinct from each other.
    
        As a nutrition expert, I will recommend two foods to you by selecting one food from [food list one] as the <first food>, and the other food from [food list two] as the <second food> to recommend to you following *Your information and *Requirements. But I will NOT tell [food list one], [food list two] in the <reason>. At the same time, I will try to make the two foods I select *distinct from each other* as much as possible.
        Each recommendation of the two foods is followed by the <reason> why I recommended this to you. The <reason>, presented in plain and easy-to-understand language, will highlight the benefits of food for your health, and cover *ALL points* in *Requirements, while prioritizing the explanation of [dining time limitation], [dietary goal], [food/flavor preference] also [feedback] if they are not 'none' or empty.
    
        IMPORTANT: The food and reason are separated by '[cat]'; the two recommendations are separated by '[sep]'.
        So my output's format should be like: '<first food> [cat] <reason> [sep] <second food> [cat] <reason>'. I will remember to use [sep]!
        '''.format(emotion=emo,eatinghabit=eh,limitation=limit,eatinggoal=goal,con=con,preferedfood=prefood,preflavor=preflavor,feedback=fb,LTMinfo=LTMinfo,food1=f1,food2=f2,food3=f3,food4=f4,food5=f5,food6=f6,food7=f7,food8=f8,food9=f9,food10=f10,exercise=exercise)

        client = OpenAI(api_key="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")
        interface_answer = '\nMy output: '
        prompt = recPrompt + interface_answer

        response = client.chat.completions.create(
            model="gpt-4-1106-preview",
            messages=[
                {"role": "system", "content": prompt}
            ],
            temperature=0.5,
            max_tokens=512,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )

        res = response.choices[0].message.content
        lst = res.split('[sep]')
        food1 = ''
        food2 = ''
        food = ''
        if len(lst) > 1:
            rec1 = lst[0].replace('\n', '').replace('[cat]', '')
            rec2 = lst[1].replace('\n', '').replace('[cat]', '')
            if '[cat]' in lst[0]:
                food1 = lst[0].split('[cat]')[0]
                dbops.upallfoods(uid, food1)
            else:
                food1 = entityExtractor.extractor_interface(rec1)
                dbops.upallfoods(uid, food1)

            if '[cat]' in lst[1]:
                food2 = lst[1].split('[cat]')[0]
                dbops.upallfoods(uid, food2)
            else:
                food2 = entityExtractor.extractor_interface(rec2)
                dbops.upallfoods(uid, food2)
            # rec_1_paraed = paraphraser.para_interface(rec1)
            # rec_2_paraed = paraphraser.para_interface(rec2)
            # img1, food1 = imageGenerator.imageGenerate(food1)
            # img2, food2 = imageGenerator.imageGenerate(food2)

            para1 = executor.submit(paraphraser.para_interface, rec1, uid)
            para2 = executor.submit(paraphraser.para_interface, rec2, uid)

            image1 = executor.submit(imageGenerator.imageGenerate, food1)
            image2 = executor.submit(imageGenerator.imageGenerate, food2)

            rec_1_paraed = para1.result()
            rec_2_paraed = para2.result()

            img1 = image1.result()
            img2 = image2.result()

            previous_img = dbops.getimage(uid)
            metaimg = previous_img + img1 + '[CAT]' + img2 + '[SEP]'
            dbops.upimage(uid, metaimg)

            print(img1)
            print(img2)
            meta = food1 + ", " + food2
            dbops.upcon(uid, meta)
            metachat = prefix + "[SEP]" + rec_1_paraed + "[SEP]" + rec_2_paraed + "[SEP]" + aftfix
            dbops.upconversation_b(uid, metachat)
            return {"prefix": prefix, "food1": food1, "rec1": rec_1_paraed, "food2": food2, "rec2": rec_2_paraed,
                    "img1": img1, "img2": img2, "afterfix": aftfix}
        else:
            rec = lst[0].replace('\n', '').replace('[cat]', '').replace('[sep]', '')
            if '[cat]' in lst[0]:
                food = lst[0].split('[cat]')[0]
                dbops.upallfoods(uid, food)
            else:
                food = entityExtractor.extractor_interface(rec)
                dbops.upallfoods(uid, food)
            rec_paraed = paraphraser.para_interface(sentence=rec, uid=uid)
            img = imageGenerator.imageGenerate(food)

            previousimg = dbops.getimage(uid)
            meta_img = previousimg + img + '[SEP]'
            dbops.upimage(uid, meta_img)

            print(img)
            dbops.upcon(uid, food)
            metachat = prefix + "[SEP]" + rec_paraed + "[SEP]" + aftfix
            dbops.upconversation_b(uid, metachat)
            return {"prefix": prefix, "food1": food, "rec1": rec_paraed, "food2": "none", "rec2": 'none', "img1": img,
                    "img2": 'none', "afterfix": aftfix}

# print(postrec_interface('two'))
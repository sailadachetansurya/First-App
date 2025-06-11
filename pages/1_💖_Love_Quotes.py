import streamlit as st # type: ignore


st.title("💖 Love Quotes")
with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.markdown('<h1 class="animated">💖 Love Quotes 💖</h1>', unsafe_allow_html=True)

st.markdown("""

---

### To,

## My Darling Princess, 👑

The reason I’m here, sitting in front of this screen on a lazy Sunday morning, is nothing short of heartwarming. My _adorable little gremlin_ 🐾 asked me to write her letters _every week_—and then had the audacity to demand both physical and digital letters! Can you even imagine the _gall_?! Utterly audacious, right? 😂 But, somehow, I love it. Actually, I had planned to write something to you earlier, but now... well, let’s just say, I’ve changed my mind, Madam Ji. 💕

Honestly, I didn’t even have anything planned for today’s letter, but yesterday, something _changed_. After seeing your love for me—no, scratch that, it's too intense to call it just love—after seeing your _desire_ for me, I was overwhelmed with so many new feelings. 🌸

**To be brutally honest**, I never thought of you as such a _needy_ woman.By needy, I mean in the sense of desiring my presence to this extent. I’ve always been under the impression that I was the only one with these random, uncontrollable urges to have you beside me, resting on the crook of your neck—not for any grand reason, but simply because _I can_. So, seeing you _pining_ for me—even if it's just because of your raging hormones—was... well, it was a feeling that hit me in the chest. I loved the idea of being _wanted_ by you, not simply _needed_. 💖

Witnessing your unbridled desire, the way you’re barely holding it together, ignited something inside me. Maybe I’m a bit twisted, but I started thinking about having you all to myself—_me and me alone_—having you pine for me, counting every second we’re apart. The thought itself was so intoxicating, it left me craving even more of your presence. 💭

But... **I don’t want to talk about love**. Yes, you heard that right, Madam Ji—I don’t want to talk about our love in this letter, because honestly, I have nothing else to say about it. It started with small things, and now it’s consumed everything, like a hungry python. 🐍 Every action you take—whether towards me or not—feels significant. I can't quite define the feeling, but I do think this is the kind of love people always talk about.

Every time I see you taking a step, or when the phone pings with your text, my heart races. But somehow, my mind calms down. A contradiction, for sure, but it’s the way I feel , I _love_ the fact that just your presence could have such a strong effect on me. Imagine what your physical presence would do to me... It makes me want to have you by my side all the time, helping me, supporting me, silently and secretly aiding me in ways I might not even notice. 🌷

This thought, this desire, it excites me—builds anticipation in my chest. It’s like a snake slithering beneath my skin—foreign, yet oddly... _comforting_? I’m not sure anymore, and honestly, I don’t care. Whatever you choose to do with me in the end is your call. _Devour me_ or _destroy me_—I’m yours to claim. 🔥

**Aaj ke liye, itna hi.** 😌

To be honest, I kind of regret saying I’d give you letters if your mock went well. What if you keep acing every single one? I mean, that’s a good problem to have, but I don’t know if I’ll be able to write you letters every single time like I’ve done. I’m left scrambling to keep up with writing you these letters every week?  You know, when I sit down to write, I pour in every bit of emotion and thought I can muster, and it usually takes me about 3 hours to get just 400 words down. It’s exhausting, but it’s _your_ reward. So here it is. 📝

💌

And don’t lie to me about your mocks, okay? I’ll be mad at you for—what—1 minute, maybe 5 minutes max? 😜 If I can’t write a letter for you one week, I’ll definitely do it the next time I have some free time. Keep doing well, and you’ll get ALL the letters from me. ✨

Sincerely,  
_Your Lovely Potential Husband_ 💍

---
""")

quotes = [
    "Love is not about how many days, months, or years you have been together. It's about how much you love each other every single day.",
    "You are the poem I never knew how to write, and this life is the story I’ve always wanted to tell.",
    "In your smile, I see something more beautiful than the stars.",
]

st.write("Here's something to warm your heart:")
for q in quotes:
    st.success(q)



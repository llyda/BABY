import os
import openai
from dotenv import load_dotenv
import pandas as pd
import json
import random

load_dotenv()

# Load your API key from a .env file
openai.api_key = os.getenv("OPEN_AI_KEY")

DOCUMENTS = [
    "I leaned against the mantel, sick, sick, Thinking of my failure, looking into the abysm, Weak from the noon-day heat. A church bell sounded mournfully far away, I heard the cry of a baby, And the coughing of John Yarnell, Bed-ridden, feverish, feverish, dying, Then the violent voice of my wife: \"Watch out, the potatoes are burning!\" I smelled them ... then there was irresistible disgust. I pulled the trigger ... blackness ... light ... Unspeakable regret ... fumbling for the world again. Too late! Thus I came here, With lungs for breathing ... one cannot breathe here with lungs, Though one must breathe Of what use is it To rid one's self of the world, When no soul may ever escape the eternal destiny of life?",
    "O, call not me to justify the wrong That thy unkindness lays upon my heart; Wound me not with thine eye but with thy tongue; Use power with power, and slay me not by art. Tell me thou lovst elsewhere; but in my sight, Dear heart, forbear to glance thine eye aside; What needst thou wound with cunning when thy might Is more than my oerpressed defense can bide? Let me excuse thee: ah, my love well knows Her pretty looks have been mine enemies; And therefore from my face she turns my foes, That they elsewhere might dart their injuries     Yet do not so; but since I am near slain,     Kill me outright with looks and rid my pain.",
    "From you have I been absent in the spring, When proud-pied April, dressed in all his trim, Hath put a spirit of youth in everything, That heavy Saturn laughed and leaped with him. Yet nor the lays of birds, nor the sweet smell Of different flowers in odour and in hue, Could make me any summers story tell, Or from their proud lap pluck them where they grew: Nor did I wonder at the lilys white, Nor praise the deep vermilion in the rose; They were but sweet, but figures of delight Drawn after you,  you pattern of all those.     Yet seemd it winter still, and, you away,     As with your shadow I with these did play.",
    "It was a lover and his lass,    With a hey, and a ho, and a hey nonino, That oer the green cornfield did pass,    In springtime, the only pretty ring time, When birds do sing, hey ding a ding, ding; Sweet lovers love the spring.  Between the acres of the rye,    With a hey, and a ho, and a hey nonino, Those pretty country folks would lie,    In springtime, the only pretty ring time, When birds do sing, hey ding a ding, ding; Sweet lovers love the spring.  This carol they began that hour,    With a hey, and a ho, and a hey nonino, How that a life was but a flower    In springtime, the only pretty ring time, When birds do sing, hey ding a ding, ding; Sweet lovers love the spring.  And therefore take the present time,    With a hey, and a ho, and a hey nonino, For love is crowned with the prime    In springtime, the only pretty ring time, When birds do sing, hey ding a ding, ding; Sweet lovers love the spring.",
    "Where be the roses gone, which sweetened so our eyes?     Where those red cheeks, which oft with fair increase did frame     The height of honor in the kindly badge of shame? Who hath the crimson weeds stolen from my morning skies? How doth the color vade of those vermilion dyes,     Which Nature's self did make, and self engrained the same!     I would know by what right this paleness overcame That hue, whose force my heart still unto thraldom ties?     Galen's adoptive sons, who by a beaten way     Their judgements hackney on, the fault on sickness lay; But feeling proof makes me say they mistake it far:     It is but love, which makes his paper perfect white     To write therein more fresh the story of delight, Whiles beauty's reddest ink Venus for him doth stir.",
    "Madam, withouten many words     Once I am sure ye will or no ... And if ye will, then leave your bourds     And use your wit and show it so, And with a beck ye shall me call;     And if of one that burneth alway Ye have any pity at all,     Answer him fair with & {.} or nay. If it be &, {.} I shall be fain;     If it be nay, friends as before; Ye shall another man obtain,     And I mine own and yours no more.",
    "Some that have deeper digg'd love's mine than I, Say, where his centric happiness doth lie;          I have lov'd, and got, and told, But should I love, get, tell, till I were old, I should not find that hidden mystery.          Oh, 'tis imposture all! And as no chemic yet th'elixir got,          But glorifies his pregnant pot          If by the way to him befall Some odoriferous thing, or medicinal,          So, lovers dream a rich and long delight,          But get a winter-seeming summer's night.  Our ease, our thrift, our honour, and our day, Shall we for this vain bubble's shadow pay?          Ends love in this, that my man Can be as happy'as I can, if he can Endure the short scorn of a bridegroom's play?          That loving wretch that swears 'Tis not the bodies marry, but the minds,          Which he in her angelic finds,          Would swear as justly that he hears, In that day's rude hoarse minstrelsy, the spheres.          Hope not for mind in women; at their best          Sweetness and wit, they'are but mummy, possess'd.",
    "I went out at night alone;  The young blood flowing beyond the sea Seemed to have drenched my spirits wings  I bore my sorrow heavily.  But when I lifted up my head  From shadows shaken on the snow, I saw Orion in the east  Burn steadily as long ago.  From windows in my fathers house,  Dreaming my dreams on winter nights, I watched Orion as a girl  Above another citys lights.  Years go, dreams go, and youth goes too,  The worlds heart breaks beneath its wars, All things are changed, save in the east  The faithful beauty of the stars.",
    "When daisies pied and violets blue       And lady-smocks all silver-white And cuckoo-buds of yellow hue       Do paint the meadows with delight, The cuckoo then, on every tree, Mocks married men; for thus sings he:                                                      Cuckoo; Cuckoo, cuckoo! O, word of fear, Unpleasing to a married ear!  When shepherds pipe on oaten straws,       And merry larks are ploughmen's clocks, When turtles tread, and rooks, and daws,       And maidens bleach their summer smocks, The cuckoo then, on every tree, Mocks married men; for thus sings he,                                                     Cuckoo; Cuckoo, cuckoo! O, word of fear, Unpleasing to a married ear!  When icicles hang by the wall,       And Dick the shepherd blows his nail, And Tom bears logs into the hall,       And milk comes frozen home in pail, When blood is nipp'd, and ways be foul, Then nightly sings the staring-owl,                                                     Tu-who; Tu-whit, tu-who!a merry note, While greasy Joan doth keel the pot.  When all aloud the wind doth blow,       And coughing drowns the parson's saw, And birds sit brooding in the snow,       And Marian's nose looks red and raw, When roasted crabs hiss in the bowl, Then nightly sings the staring owl,                                                     Tu-who; Tu-whit, tu-who!a merry note, While greasy Joan doth keel the pot.",
    "Her terrace was the sand And the palms and the twilight.   She made of the motions of her wrist The grandiose gestures Of her thought.   The rumpling of the plumes Of this creature of the evening Came to be sleights of sails Over the sea.   And thus she roamed In the roamings of her fan,  Partaking of the sea, And of the evening, As they flowed around And uttered their subsiding sound.",
    "Stella, since thou so right a princess art Of all the powers which life bestows on me, There ere by them aught undertaken be They first resort unto that sovereign part; Sweet, for a while give respite to my heart, Which pants as though it still should leap to thee, And on my thoughts give thy lieutenancy To this great cause, which needs both use and art, And as a queen, who from her presence sends Whom she employs, dismiss from thee my wit, Till it have wrought what thy own will attends. On servants shame oft masters blame doth sit. Oh let not fools in me thy works reprove, And scorning say, See what it is to love.",
    "from Coterie, 1919",
    "Gertrude Stein, [The house was twinkling in the moon light] from Baby Precious Always Shines: Selected Love Notes Between Gertrude Stein and Alice B. Toklas (St. Martins Press, 1999). Reprinted with the permission of the Estate of Gertrude Stein.",
    "Lucks, my fair falcon, and your fellows all,    How well pleasant it were your liberty! Ye not forsake me that fair might ye befall. But they that sometime liked my company: Like lice away from dead bodies they crawl. Lo what a proof in light adversity! But ye my birds, I swear by all your bells, Ye be my friends, and so be but few else.",
    "No longer mourn for me when I am dead Than you shall hear the surly sullen bell Give warning to the world that I am fled From this vile world with vilest worms to dwell;  Nay, if you read this line, remember not The hand that writ it; for I love you so,  That I in your sweet thoughts would be forgot,  If thinking on me then should make you woe. O, if (I say) you look upon this verse,  When I (perhaps) compounded am with clay, Do not so much as my poor name rehearse, But let your love even with my life decay, Lest the wise world should look into your moan,  And mock you with me after I am gone.",
    "Originally published in Poetry, March 1914.",
    "Come, my Celia, let us prove, While we can, the sports of love; Time will not be ours forever; He at length our good will sever. Spend not then his gifts in vain. Suns that set may rise again; But if once we lose this light, Tis with us perpetual night. Why should we defer our joys? Fame and rumor are but toys. Cannot we delude the eyes Of a few poor household spies, Or his easier ears beguile, So removed by our wile? Tis no sin loves fruit to steal; But the sweet thefts to reveal, To be taken, to be seen, These have crimes accounted been.",
    "Maurice, weep not, I am not here under this pine tree. The balmy air of spring whispers through the sweet grass, The stars sparkle, the whippoorwill calls, But thou grievest, while my soul lies rapturous In the blest Nirvana of eternal light! Go to the good heart that is my husband, Who broods upon what he calls our guilty love: i Tell him that my love for you, no less than my love for him Wrought out my destiny i that through the flesh I won spirit, and through spirit, peace. There is no marriage in heaven, But there is love.",
    "Only the wanderer    Knows England's graces, Or can anew see clear    Familiar faces.  And who loves joy as he    That dwells in shadows? Do not forget me quite,    O Severn meadows.",
    "Hugh MacDiarmid, Stony Limits from Selected Poetry. Copyright  1992 by Alan Riach and Michael Grieve. Reprinted with the permission of New Directions Publishing Corporation.",
    "Weret aught to me I bore the canopy, With my extern the outward honouring, Or laid great bases for eternity, Which proves more short than waste or ruining; Have I not seen dwellers on form and favour Lose all, and more, by paying too much rent, For compound sweet forgoing simple savour, Pitiful thrivers, in their gazing spent? No;let me be obsequious in thy heart, And take thou my oblation, poor but free, Which is not mixd with seconds, knows no art, But mutual render, only me for thee.    Hence, thou subornd informer! a true soul,    When most impeachd, stands least in thy control.   ",
    "Michael Anania, Memorial Day from Selected Poems. Copyright  1994 by Michael Anania. Used by permission of Asphodel Press/Acorn Alliance.",
    "Hart Crane, \"Cutty Sark\" from The Complete Poems of Hart Crane, edited by Marc SImon. Copyright  1933, 1958, 1966 by Liveright Publishing Corporation. Copyright  1986 by Marc Simon. Used by permission of Liveright Publishing.",
    "Fayre is my love, when her fayre golden heares, With the loose wynd ye waving chance to marke: Fayre when the rose in her red cheekes appears, Or in her eyes the fyre of love does sparke. Fayre when her brest lyke a rich laden barke, With pretious merchandize she forth doth lay: Fayre when that cloud of pryde which oft doth dark Her goodly light with smiles she drives away, But fayrest she, when so she doth display The gate with pearles and rubyes richly dight: Throgh which her words so wise do make their way To beare the message of her gentle spright. The rest be works of natures wonderment, But this the worke of harts astonishment.",
    "A face that should content me wondrous well Should not be fair but lovely to behold, With gladsome cheer all grief for to expel; With sober looks so would I that it should Speak without words such words as none can tell; Her tress also should be of crisped gold; With wit; and thus might chance I might be tied, And knit again the knot that should not slide.",
    "W. B. Yeats, Lapis Lazuli from The Poems of W. B. Yeats: A New Edition, edited by Richard J. Finneran. Copyright 1933 by Macmillan Publishing Company, renewed  1961 by Georgie Yeats. Reprinted with the permission of A. P. Watt, Ltd. on behalf of Michael Yeats.",
    "When thou must home to shades of underground, And there arriv'd, a new admired guest, The beauteous spirits do engirt thee round, White Iope, blithe Helen, and the rest, To hear the stories of thy finish'd love From that smooth tongue whose music hell can move;  Then wilt thou speak of banqueting delights, Of masques and revels which sweet youth did make, Of tourneys and great challenges of knights, And all these triumphs for thy beauty's sake: When thou hast told these honours done to thee, Then tell, O tell, how thou didst murder me.",
    "Let me not to the marriage of true minds Admit impediments. Love is not love Which alters when it alteration finds, Or bends with the remover to remove. O no! it is an ever-fixed mark That looks on tempests and is never shaken; It is the star to every wand'ring bark, Whose worth's unknown, although his height be taken. Love's not Time's fool, though rosy lips and cheeks Within his bending sickle's compass come; Love alters not with his brief hours and weeks, But bears it out even to the edge of doom. If this be error and upon me prov'd, I never writ, nor no man ever lov'd.",
    "If it were not for England, who would bear This heavy servitude one moment more? To keep a brothel, sweep and wash the floor Of filthiest hovels were noble to compare With this brass-cleaning life. Now here, now there Harried in foolishness, scanned curiously o'er By fools made brazen by conceit, and store Of antique witticisms thin and bare.  Only the love of comrades sweetens all, Whose laughing spirit will not be outdone. As night-watching men wait for the sun To hearten them, so wait I on such boys As neither brass nor Hell-fire may appal, Nor guns, nor sergeant-major's bluster and noise.",
    "I went out to the hazel wood, Because a fire was in my head, And cut and peeled a hazel wand, And hooked a berry to a thread; And when white moths were on the wing, And moth-like stars were flickering out, I dropped the berry in a stream And caught a little silver trout.  When I had laid it on the floor I went to blow the fire a-flame, But something rustled on the floor, And someone called me by my name: It had become a glimmering girl With apple blossom in her hair Who called me by my name and ran And faded through the brightening air.  Though I am old with wandering Through hollow lands and hilly lands, I will find out where she has gone, And kiss her lips and take her hands; And walk among long dappled grass, And pluck till time and times are done, The silver apples of the moon, The golden apples of the sun.",
    "Being your slave, what should I do but tend Upon the hours and times of your desire? I have no precious time at all to spend, Nor services to do, till you require. Nor dare I chide the world-without-end hour Whilst I, my sovereign, watch the clock for you. Nor think the bitterness of absence sour When you have bid your servant once adieu; Nor dare I question with my jealous thought Where you may be, or your affairs suppose, But like a sad slave, stay and think of nought, Save, where you are how happy you make those. So true a fool is love that in your will Though you do anything, he thinks no ill.",
    "Farewell love and all thy laws forever; Thy baited hooks shall tangle me no more. Senec and Plato call me from thy lore To perfect wealth, my wit for to endeavour. In blind error when I did persever, Thy sharp repulse, that pricketh aye so sore, Hath taught me to set in trifles no store And scape forth, since liberty is lever. Therefore farewell; go trouble younger hearts And in me claim no more authority. With idle youth go use thy property And thereon spend thy many brittle darts, For hitherto though I have lost all my time, Me lusteth no lenger rotten boughs to climb.",
    "Lying in dug-outs, joking idly, wearily;    Watching the candle guttering in the draught; Hearing the great shells go high over us, eerily    Singing; how often have I turned over, and laughed   With pity and pride, photographs of all colours,    All sizes, subjects: khaki brothers in France; Or mother's faces worn with countless dolours;    Or girls whose eyes were challenging and must dance,   Though in a picture only, a common cheap    Ill-taken card; and childrenfrozen, some (Babies) waiting on Dicky-bird to peep    Out of the handkerchief that is his home   (But he's so shy!). And some with bright looks, calling    Delight across the miles of land and sea, That not the dread of barrage suddenly falling    Could quite blot outnot mud nor lethargy.   Smiles and triumphant careless laughter. O    The pain of them, wide Earth's most sacred things!  Lying in dug-outs, hearing the great shells slow    Sailing mile-high, the heart mounts higher and sings.   But onceO why did he keep that bitter token    Of a dead Love?that boy, who, suddenly moved, Showed me, his eyes wet, his low talk broken,    A girl who better had not been beloved.",
    "Loving in truth, and fain in verse my love to show, That she, dear she, might take some pleasure of my pain, Pleasure might cause her read, reading might make her know, Knowledge might pity win, and pity grace obtain, I sought fit words to paint the blackest face of woe; Studying inventions fine her wits to entertain, Oft turning others' leaves, to see if thence would flow Some fresh and fruitful showers upon my sunburn'd brain. But words came halting forth, wanting invention's stay; Invention, Nature's child, fled step-dame Study's blows; And others' feet still seem'd but strangers in my way. Thus great with child to speak and helpless in my throes, Biting my truant pen, beating myself for spite, \"Fool,\" said my Muse to me, \"look in thy heart, and write.\"",
    "Come live with me, and be my love, And we will some new pleasures prove Of golden sands, and crystal brooks, With silken lines, and silver hooks.  There will the river whispering run Warm'd by thy eyes, more than the sun; And there the 'enamour'd fish will stay, Begging themselves they may betray.  When thou wilt swim in that live bath, Each fish, which every channel hath, Will amorously to thee swim, Gladder to catch thee, than thou him.  If thou, to be so seen, be'st loth, By sun or moon, thou dark'nest both, And if myself have leave to see, I need not their light having thee.  Let others freeze with angling reeds, And cut their legs with shells and weeds, Or treacherously poor fish beset, With strangling snare, or windowy net.  Let coarse bold hands from slimy nest The bedded fish in banks out-wrest; Or curious traitors, sleeve-silk flies, Bewitch poor fishes' wand'ring eyes.  For thee, thou need'st no such deceit, For thou thyself art thine own bait: That fish, that is not catch'd thereby, Alas, is wiser far than I.",
    "Hart Crane, \"Voyages I, II, III, IV, V, VI\" from The Complete Poems of Hart Crane, edited by Marc Simon. Copyright  1933, 1958, 1966 by Liveright Publishing Corporation. Copyright  1986 by Marc Simon. Used by permission of Liveright Publishing.",
    "I have sat here happy in the gardens, Watching the still pool and the reeds And the dark clouds Which the wind of the upper air Tore like the green leafy boughs Of the divers-hued trees of late summer; But though I greatly delight In these and the water-lilies, That which sets me nighest to weeping Is the rose and white color of the smooth flag-stones, And the pale yellow grasses Among them.",
    "When I remember plain heroic strength And shining virtue shown by Ypres pools, Then read the blither written by knaves for fools In praise of English soldiers lying at length, Who purely dream what England shall be made Gloriously new, free of the old stains By us, who pay the price that must be paid, Will freeze all winter over Ypres plains. Our silly dreams of peace you put aside And brotherhood of man, for you will see An armed mistress, braggart of the tide, Her children slaves, under your mastery. We'll have a word there too, and forge a knife, Will cut the cancer threatens England's life.",
    "Stand still, and I will read to thee A lecture, love, in love's philosophy.          These three hours that we have spent,          Walking here, two shadows went Along with us, which we ourselves produc'd. But, now the sun is just above our head,          We do those shadows tread,          And to brave clearness all things are reduc'd. So whilst our infant loves did grow, Disguises did, and shadows, flow From us, and our cares; but now 'tis not so. That love has not attain'd the high'st degree, Which is still diligent lest others see.  Except our loves at this noon stay, We shall new shadows make the other way.          As the first were made to blind          Others, these which come behind Will work upon ourselves, and blind our eyes. If our loves faint, and westwardly decline,          To me thou, falsely, thine,          And I to thee mine actions shall disguise. The morning shadows wear away, But these grow longer all the day; But oh, love's day is short, if love decay. Love is a growing, or full constant light, And his first minute, after noon, is night.",
    "Copyright  1996 by the Estate of Mina Loy. All rights reserved.",
    "If thou survive my well-contented day, When that churl Death my bones with dust shall cover, And shalt by fortune once more re-survey These poor rude lines of thy deceased lover, Compare them with the bettering of the time, And though they be outstripp'd by every pen, Reserve them for my love, not for their rhyme, Exceeded by the height of happier men. O then vouchsafe me but this loving thought: \"Had my friend's Muse grown with this growing age A dearer birth than this his love had brought, To march in ranks of better equipage: But since he died and poets better prove, Theirs for their style I'll read, his for his love.\"",
    "Hugh MacDiarmid, The Watergaw from Selected Poetry. Copyright  1992 by Alan Riach and Michael Grieve. Reprinted with the permission of New Directions Publishing Corporation.",
    "There may be chaos still around the world, This little world that in my thinking lies; For mine own bosom is the paradise Where all my lifes fair visions are unfurled. Within my natures shell I slumber curled, Unmindful of the changing outer skies, Where now, perchance, some new-born Eros flies, Or some old Cronos from his throne is hurled. I heed them not; or if the subtle night Haunt me with deities I never saw, I soon mine eyelids drowsy curtain draw To hide their myriad faces from my sight. They threat in vain; the whirlwind cannot awe A happy snow-flake dancing in the flaw.",
    "My Love is like to ice, and I to fire: How comes it then that this her cold so great Is not dissolved through my so hot desire, But harder grows the more I her entreat? Or how comes it that my exceeding heat Is not allayed by her heart-frozen cold, But that I burn much more in boiling sweat, And feel my flames augmented manifold? What more miraculous thing may be told, That fire, which all things melts, should harden ice, And ice, which is congeald with senseless cold, Should kindle fire by wonderful device? Such is the power of love in gentle mind, That it can alter all the course of kind.",
    "When I was fair and young, then favor graced me. Of many was I sought their mistress for to be. But I did scorn them all and answered them therefore: Go, go, go, seek some other where; importune me no more.  How many weeping eyes I made to pine in woe, How many sighing hearts I have not skill to show, But I the prouder grew and still this spake therefore: Go, go, go, seek some other where, importune me no more.  Then spake fair Venus son, that proud victorious boy, Saying: You dainty dame, for that you be so coy, I will so pluck your plumes as you shall say no more: Go, go, go, seek some other where, importune me no more.  As soon as he had said, such change grew in my breast That neither night nor day I could take any rest. Wherefore I did repent that I had said before: Go, go, go, seek some other where, importune me no more.",
    "Misus and Mopsa hardly could agree, Striving about superiority. The text which says that man and wife are one, Was the chief argument they stood upon.  She held they both one woman should become, He held both should be man, and both but one.      So they contended daily, but the strife      Could not be ended, till both were one wife.",
    "If yet I have not all thy love, Dear, I shall never have it all; I cannot breathe one other sigh, to move, Nor can intreat one other tear to fall; And all my treasure, which should purchase thee Sighs, tears, and oaths, and lettersI have spent. Yet no more can be due to me, Than at the bargain made was meant; If then thy gift of love were partial, That some to me, some should to others fall,          Dear, I shall never have thee all.  Or if then thou gavest me all, All was but all, which thou hadst then; But if in thy heart, since, there be or shall New love created be, by other men, Which have their stocks entire, and can in tears, In sighs, in oaths, and letters, outbid me, This new love may beget new fears, For this love was not vow'd by thee. And yet it was, thy gift being general; The ground, thy heart, is mine; whatever shall          Grow there, dear, I should have it all.  Yet I would not have all yet, He that hath all can have no more; And since my love doth every day admit New growth, thou shouldst have new rewards in store; Thou canst not every day give me thy heart, If thou canst give it, then thou never gavest it; Love's riddles are, that though thy heart depart, It stays at home, and thou with losing savest it; But we will have a way more liberal, Than changing hearts, to join them; so we shall          Be one, and one another's all.",
    "My sweetest Lesbia, let us live and love, And though the sager sort our deeds reprove, Let us not weigh them. Heavens great lamps do dive Into their west, and straight again revive, But soon as once set is our little light, Then must we sleep one ever-during night.  If all would lead their lives in love like me, Then bloody swords and armor should not be; No drum nor trumpet peaceful sleeps should move, Unless alarm came from the camp of love. But fools do live, and waste their little light, And seek with pain their ever-during night.  When timely death my life and fortune ends, Let not my hearse be vexed with mourning friends, But let all lovers, rich in triumph, come And with sweet pastimes grace my happy tomb; And Lesbia, close up thou my little light, And crown with love my ever-during night.",
    "Not in that wasted garden Where bodies are drawn into grass That feeds no flocks, and into evergreens That bear no fruit  There where along the shaded walks Vain sighs are heard, And vainer dreams are dreamed Of close communion with departed souls  But here under the apple tree I loved and watched and pruned With gnarled hands In the long, long years; Here under the roots of this northern-spy To move in the chemic change and circle of life, Into the soil and into the flesh of the tree, And into the living epitaphs Of redder apples!",
    "Praisd be Dianas fair and harmless light; Praisd be the dews wherewith she moists the ground; Praisd be her beams, the glory of the night; Praisd be her power by which all powers abound.  Praisd be her nymphs with whom she decks the woods, Praisd be her knights in whom true honour lives; Praisd be that force by which she moves the floods; Let that Diana shine which all these gives.  In heaven queen she is among the spheres; In aye she mistress-like makes all things pure; Eternity in her oft change she bears; She beauty is; by her the fair endure.  Time wears her not: she doth his chariot guide; Mortality below her orb is placd; By her the virtue of the stars down slide; In her is virtues perfect image cast.           A knowledge pure it is her worth to know:          With Circes let them dwell that think not so."
]
EXAMPLES = [
    [
        "Write a poem like william shakespeare",
        "When I have seen by Time's fell hand defac'd The rich proud cost of outworn buried age; When sometime lofty towers I see down-ras'd And brass eternal slave to mortal rage; When I have seen the hungry ocean gain Advantage on the kingdom of the shore, And the firm soil win of the wat'ry main, Increasing store with loss and loss with store; When I have seen such interchange of state, Or state itself confounded to decay; Ruin hath taught me thus to ruminate, That Time will come and take my love away. This thought is as a death, which cannot choose But weep to have that which it fears to lose."
    ],
    [
        "Write a poem like queen elizabeth i",
        "When I was fair and young, then favor graced me. Of many was I sought their mistress for to be. But I did scorn them all and answered them therefore: Go, go, go, seek some other where; importune me no more.  How many weeping eyes I made to pine in woe, How many sighing hearts I have not skill to show, But I the prouder grew and still this spake therefore: Go, go, go, seek some other where, importune me no more.  Then spake fair Venus son, that proud victorious boy, Saying: You dainty dame, for that you be so coy, I will so pluck your plumes as you shall say no more: Go, go, go, seek some other where, importune me no more.  As soon as he had said, such change grew in my breast That neither night nor day I could take any rest. Wherefore I did repent that I had said before: Go, go, go, seek some other where, importune me no more."
    ],
    [
        "Write a poem like edmund spenser",
        "The sovereign beauty which I do admire, Witness the world how worthy to be praised: The light whereof hath kindled heavenly fire In my frail spirit, by her from baseness raised; That being now with her huge brightness dazed, Base thing I can no more endure to view; But looking still on her, I stand amazed At wondrous sight of so celestial hue. So when my tongue would speak her praises due, It stopped is with thought's astonishment: And when my pen would write her titles true, It ravish'd is with fancy's wonderment: Yet in my heart I then both speak and write The wonder that my wit cannot endite."
    ],
    [
        "Write a poem like michael anania",
        "Michael Anania, Memorial Day from Selected Poems. Copyright  1994 by Michael Anania. Used by permission of Asphodel Press/Acorn Alliance."
    ],
    [
        "Write a poem like william shakespeare",
        "What is your substance, whereof are you made, That millions of strange shadows on you tend? Since every one hath, every one, one shade, And you, but one, can every shadow lend. Describe Adonis, and the counterfeit Is poorly imitated after you; On Helen's cheek all art of beauty set, And you in Grecian tires are painted new. Speak of the spring and foison of the year: The one doth shadow of your beauty show, The other as your bounty doth appear; And you in every blessed shape we know.     In all external grace you have some part,     But you like none, none you, for constant heart."
    ],
    [
        "Write a poem like john donne",
        "Tis true, tis day, what though it be? O wilt thou therefore rise from me? Why should we rise because tis light? Did we lie down because twas night? Love, which in spite of darkness brought us hither, Should in despite of light keep us together.  Light hath no tongue, but is all eye; If it could speak as well as spy, This were the worst that it could say, That being well I fain would stay, And that I loved my heart and honour so, That I would not from him, that had them, go.  Must business thee from hence remove? Oh, thats the worst disease of love, The poor, the foul, the false, love can Admit, but not the busied man. He which hath business, and makes love, doth do Such wrong, as when a married man doth woo."
    ],
    [
        "Write a poem like louise bogan",
        "Louise Bogan, Song for the Last Act from The Blue Estuaries: Poems 1923-1968. Copyright  1968 by Louise Bogan. Used by permission of Farrar, Straus & Giroux, LLC, http://us.macmillan.com/fsg. All rights reserved."
    ],
    [
        "Write a poem like john skelton",
        "Womanhood, wanton, ye want: Your meddling, mistress, is mannerless; Plenty of ill, of goodness scant, Ye rail at riot, reckless: To praise your port it is needless; For all your draff yet and your dregs, As well borne as ye full oft time begs.  Why so coy and full of scorn? Mine horse is sold, I ween, you say; My new furred gown, when it is worn... Put up your purse, ye shall not pay! By crede, I trust to see the day, As proud a pea-hen as ye spread, Of me and other ye may have need!  Though angelic be your smiling, Yet is your tongue an adders tail, Full like a scorpion stinging All those by whom ye have avail. Good mistress Anne, there ye do shail: What prate ye, pretty pigesnye? I trust to quite you ere I die!  Your key is meet for every lock, Your key is common and hangeth out; Your key is ready, we need not knock, Nor stand long wresting there about; Of your door-gate ye have no doubt: But one thing is, that ye be lewd: Hold your tongue now, all beshrewd!  To mistress Anne, that farly sweet, That wones at The Key in Thames Street.  "
    ],
    [
        "Write a poem like william butler yeats",
        "The jester walked in the garden: The garden had fallen still; He bade his soul rise upward And stand on her window-sill.  It rose in a straight blue garment, When owls began to call: It had grown wise-tongued by thinking Of a quiet and light footfall;  But the young queen would not listen; She rose in her pale night-gown; She drew in the heavy casement And pushed the latches down.  He bade his heart go to her, When the owls called out no more; In a red and quivering garment It sang to her through the door.  It had grown sweet-tongued by dreaming Of a flutter of flower-like hair; But she took up her fan from the table And waved it off on the air.  'I have cap and bells, he pondered, 'I will send them to her and die; And when the morning whitened He left them where she went by.  She laid them upon her bosom, Under a cloud of her hair, And her red lips sang them a love-song Till stars grew out of the air.  She opened her door and her window, And the heart and the soul came through, To her right hand came the red one, To her left hand came the blue.  They set up a noise like crickets, A chattering wise and sweet, And her hair was a folded flower And the quiet of love in her feet."
    ],
    [
        "Write a poem like sara teasdale",
        "Originally published in Poetry, March 1914."
    ],
    [
        "Write a poem like william butler yeats",
        "I went out to the hazel wood, Because a fire was in my head, And cut and peeled a hazel wand, And hooked a berry to a thread; And when white moths were on the wing, And moth-like stars were flickering out, I dropped the berry in a stream And caught a little silver trout.  When I had laid it on the floor I went to blow the fire a-flame, But something rustled on the floor, And someone called me by my name: It had become a glimmering girl With apple blossom in her hair Who called me by my name and ran And faded through the brightening air.  Though I am old with wandering Through hollow lands and hilly lands, I will find out where she has gone, And kiss her lips and take her hands; And walk among long dappled grass, And pluck till time and times are done, The silver apples of the moon, The golden apples of the sun."
    ],
    [
        "Write a poem like wallace stevens",
        "You dweller in the dark cabin, To whom the watermelon is always purple,    Whose garden is wind and moon,  Of the two dreams, night and day, What lover, what dreamer, would choose    The one obscured by sleep?  Here is the plantain by your door    And the best cock of red feather    That crew before the clocks.  A feme may come, leaf-green,    Whose coming may give revel    Beyond revelries of sleep,  Yes, and the blackbird spread its tail,    So that the sun may speckle,    While it creaks hail.  You dweller in the dark cabin,    Rise, since rising will not waken,    And hail, cry hail, cry hail."
    ],
    [
        "Write a poem like katherine mansfield",
        "But then there comes that moment rare When, for no cause that I can find, The little voices of the air Sound above all the sea and wind.  The sea and wind do then obey And sighing, sighing double notes Of double basses, content to play A droning chord for the little throats  The little throats that sing and rise Up into the light with lovely ease And a kind of magical, sweet surprise To hear and know themselves for these  For these little voices: the bee, the fly, The leaf that taps, the pod that breaks, The breeze on the grass-tops bending by, The shrill quick sound that the insect makes."
    ],
    [
        "Write a poem like sir walter ralegh",
        "Praisd be Dianas fair and harmless light; Praisd be the dews wherewith she moists the ground; Praisd be her beams, the glory of the night; Praisd be her power by which all powers abound.  Praisd be her nymphs with whom she decks the woods, Praisd be her knights in whom true honour lives; Praisd be that force by which she moves the floods; Let that Diana shine which all these gives.  In heaven queen she is among the spheres; In aye she mistress-like makes all things pure; Eternity in her oft change she bears; She beauty is; by her the fair endure.  Time wears her not: she doth his chariot guide; Mortality below her orb is placd; By her the virtue of the stars down slide; In her is virtues perfect image cast.           A knowledge pure it is her worth to know:          With Circes let them dwell that think not so."
    ],
    [
        "Write a poem like asil bunting",
        "Basil Bunting, Briggflatts (Part 1) from Complete Poems, edited by Richard Caddel. Reprinted with the permission of Bloodaxe Books Ltd., www.bloodaxebooks.com."
    ],
    [
        "Write a poem like guillaume apollinaire",
        "I have built a house in the middle of the Ocean Its windows are the rivers flowing from my eyes Octopi are crawling all over where the walls are Hear their triple hearts beat and their beaks peck against the windowpanes  House of dampness House of burning Seasons fastness Season singing The airplanes are laying eggs Watch out for the dropping of the anchor  Watch out for the shooting black ichor It would be good if you were to come from the sky The skys honeysuckle is climbing The earthly octopi are throbbing And so very many of us have become our own gravediggers Pale octopi of the chalky waves O octopi with pale beaks Around the house is this ocean that you know well   And is never still   Translated from the French "
    ],
    [
        "Write a poem like christopher marlowe",
        "Come live with me and be my love, And we will all the pleasures prove, That Valleys, groves, hills, and fields, Woods, or steepy mountain yields.  And we will sit upon the Rocks, Seeing the Shepherds feed their flocks, By shallow Rivers to whose falls Melodious birds sing Madrigals.  And I will make thee beds of Roses And a thousand fragrant posies, A cap of flowers, and a kirtle Embroidered all with leaves of Myrtle;  A gown made of the finest wool Which from our pretty Lambs we pull; Fair lined slippers for the cold, With buckles of the purest gold;  A belt of straw and Ivy buds, With Coral clasps and Amber studs: And if these pleasures may thee move, Come live with me, and be my love.  The Shepherds Swains shall dance and sing For thy delight each May-morning: If these delights thy mind may move, Then live with me, and be my love."
    ],
    [
        "Write a poem like william shakespeare",
        "Full many a glorious morning have I seen Flatter the mountain-tops with sovereign eye, Kissing with golden face the meadows green, Gilding pale streams with heavenly alchemy; Anon permit the basest clouds to ride With ugly rack on his celestial face And from the forlorn world his visage hide, Stealing unseen to west with this disgrace. Even so my sun one early morn did shine With all-triumphant splendour on my brow; But out, alack! he was but one hour mine; The region cloud hath mask'd him from me now. Yet him for this my love no whit disdaineth; Suns of the world may stain when heaven's sun staineth."
    ],
    [
        "Write a poem like sir thomas wyatt",
        "What needeth these threnning words and wasted wind? All this cannot make me restore my prey. To rob your good, iwis, is not my mind, Nor causeless your fair hand did I display. Let love be judge or else whom next we meet That may both hear what you and I can say: She took from me an heart, and I a glove from her. Let us see now if th'one be worth th'other."
    ],
    [
        "Write a poem like richard aldington",
        "Potuia, potuia White grave goddess, Pity my sadness, O silence of Paros.  I am not of these about thy feet, These garments and decorum; I am thy brother, Thy lover of aforetime crying to thee, And thou hearest me not.  I have whispered thee in thy solitudes Of our loves in Phrygia, The far ecstasy of burning noons When the fragile pipes Ceased in the cypress shade, And the brown fingers of the shepherd Moved over slim shoulders; And only the cicada sang.  I have told thee of the hills And the lisp of reeds And the sun upon thy breasts,  And thou hearest me not, Potuia, potuia Thou hearest me not."
    ],
    [
        "Write a poem like john donne",
        "As virtuous men pass mildly away,    And whisper to their souls to go, Whilst some of their sad friends do say    The breath goes now, and some say, No:  So let us melt, and make no noise,    No tear-floods, nor sigh-tempests move; 'Twere profanation of our joys    To tell the laity our love.  Moving of th' earth brings harms and fears,    Men reckon what it did, and meant; But trepidation of the spheres,    Though greater far, is innocent.  Dull sublunary lovers' love    (Whose soul is sense) cannot admit Absence, because it doth remove    Those things which elemented it.  But we by a love so much refined,    That our selves know not what it is, Inter-assured of the mind,    Care less, eyes, lips, and hands to miss.  Our two souls therefore, which are one,    Though I must go, endure not yet A breach, but an expansion,    Like gold to airy thinness beat.  If they be two, they are two so    As stiff twin compasses are two; Thy soul, the fixed foot, makes no show    To move, but doth, if the other do.  And though it in the center sit,    Yet when the other far doth roam, It leans and hearkens after it,    And grows erect, as that comes home.  Such wilt thou be to me, who must,    Like th' other foot, obliquely run; Thy firmness makes my circle just,    And makes me end where I begun."
    ],
    [
        "Write a poem like wallace stevens",
        "As the immense dew of Florida Brings forth The big-finned palm And green vine angering for life,   As the immense dew of Florida Brings forth hymn and hymn From the beholder, Beholding all these green sides And gold sides of green sides,   And blessed mornings, Meet for the eye of the young alligator, And lightning colors So, in me, come flinging Forms, flames, and the flakes of flames."
    ],
    [
        "Write a poem like sir philip sidney",
        "With how sad steps, O Moon, thou climb'st the skies! How silently, and with how wan a face! What, may it be that even in heav'nly place That busy archer his sharp arrows tries! Sure, if that long-with love-acquainted eyes Can judge of love, thou feel'st a lover's case, I read it in thy looks; thy languish'd grace To me, that feel the like, thy state descries. Then, ev'n of fellowship, O Moon, tell me, Is constant love deem'd there but want of wit? Are beauties there as proud as here they be? Do they above love to be lov'd, and yet Those lovers scorn whom that love doth possess? Do they call virtue there ungratefulness?"
    ],
    [
        "Write a poem like william butler yeats",
        "Wine comes in at the mouth And love comes in at the eye; Thats all we shall know for truth Before we grow old and die. I lift the glass to my mouth, I look at you, and I sigh."
    ],
    [
        "Write a poem like samuel daniel",
        "Love is a sickness full of woes, All remedies refusing; A plant that with most cutting grows, Most barren with best using. Why so? More we enjoy it, more it dies; If not enjoyed, it sighting cries, Heigh ho!  Love is a torment of the mind, A tempest everlasting; And Jove hath made it of a kind Not well, not full, nor fasting. Why so? More we enjoy it, more it dies; If not enjoyed, it sighing cries, Heigh ho!"
    ],
    [
        "Write a poem like sir philip sidney",
        "Come Sleep! O Sleep, the certain knot of peace, The baiting-place of wit, the balm of woe, The poor man's wealth, the prisoner's release, Th' indifferent judge between the high and low. With shield of proof shield me from out the prease Of those fierce darts despair at me doth throw: O make in me those civil wars to cease; I will good tribute pay, if thou do so. Take thou of me smooth pillows, sweetest bed, A chamber deaf to noise and blind to light, A rosy garland and a weary head: And if these things, as being thine by right, Move not thy heavy grace, thou shalt in me, Livelier than elsewhere, Stella's image see."
    ],
    [
        "Write a poem like edmund spenser",
        "Lyke as the Culver on the bared bough, Sits mourning for the absence of her mate: And in her songs sends many a wishfull vow, For his returne that seemes to linger late, So I alone now left disconsolate, Mourne to my selfe the absence of my love: And wandring here and there all desolate, Seek with my playnts to match that mournful dove: Ne joy of ought that under heaven doth hove, Can comfort me, but her owne joyous sight: Whose sweet aspect both God and man can move, In her unspotted pleasauns to delight. Dark is my day, whyles her fayre light I mis, And dead my life that wants such lively blis."
    ],
    [
        "Write a poem like sir philip sidney",
        "Souls joy, bend not those morning stars from me, Where virtue is made strong by beautys might, Where love is chasteness, pain doth learn delight, And humbleness grows one with majesty. Whatever may ensue, O let me be Co-partner of the riches of that sight; Let not mine eyes be hell-drivn from that light; O look, O shine, O let me die and see. For though I oft my self of them bemoan, That through my heart their beamy darts be gone, Whose cureless wounds even now most freshly bleed, Yet since my death wound is already got, Dear killer, spare not they sweet cruel shot; A kind of grace it is to slay with speed."
    ],
    [
        "Write a poem like carl sandburg",
        "Passing through huddled and ugly walls, By doorways where women haggard Looked from their hunger-deep eyes, Haunted with shadows of hunger-hands, Out from the huddled and ugly walls, I came sudden, at the city's edge, On a blue burst of lake, Long lake waves breaking under the sun On a spray-flung curve of shore; And a fluttering storm of gulls, Masses of great gray wings And flying white bellies Veering and wheeling free in the open."
    ],
    [
        "Write a poem like john donne",
        "Twice or thrice had I lov'd thee, Before I knew thy face or name; So in a voice, so in a shapeless flame Angels affect us oft, and worshipp'd be;          Still when, to where thou wert, I came, Some lovely glorious nothing I did see.          But since my soul, whose child love is, Takes limbs of flesh, and else could nothing do,          More subtle than the parent is Love must not be, but take a body too;          And therefore what thou wert, and who,                 I bid Love ask, and now That it assume thy body, I allow, And fix itself in thy lip, eye, and brow.  Whilst thus to ballast love I thought, And so more steadily to have gone, With wares which would sink admiration, I saw I had love's pinnace overfraught;          Ev'ry thy hair for love to work upon Is much too much, some fitter must be sought;          For, nor in nothing, nor in things Extreme, and scatt'ring bright, can love inhere;          Then, as an angel, face, and wings Of air, not pure as it, yet pure, doth wear,          So thy love may be my love's sphere;                 Just such disparity As is 'twixt air and angels' purity, 'Twixt women's love, and men's, will ever be."
    ],
    [
        "Write a poem like john donne",
        "Here take my picture; though I bid farewell Thine, in my heart, where my soul dwells, shall dwell. 'Tis like me now, but I dead, 'twill be more When we are shadows both, than 'twas before. When weather-beaten I come back, my hand Perhaps with rude oars torn, or sun beams tann'd, My face and breast of haircloth, and my head With care's rash sudden storms being o'erspread, My body'a sack of bones, broken within, And powder's blue stains scatter'd on my skin; If rival fools tax thee to'have lov'd a man So foul and coarse as, oh, I may seem then, This shall say what I was, and thou shalt say, \"Do his hurts reach me? doth my worth decay? Or do they reach his judging mind, that he Should now love less, what he did love to see? That which in him was fair and delicate, Was but the milk which in love's childish state Did nurse it; who now is grown strong enough To feed on that, which to disus'd tastes seems tough.\""
    ],
    [
        "Write a poem like samuel daniel",
        "Unto the boundless Ocean of thy beauty Runs this poor river, charged with streams of zeal: Returning thee the tribute of my duty, Which here my love, my youth, my plaints reveal. Here I unclasp the book of my charged soul, Where I have cast th'accounts of all my care: Here have I summed my sighs, here I enroll How they were spent for thee; look what they are. Look on the dear expenses of my youth, And see how just I reckon with thine eyes: Examine well thy beauty with my truth, And cross my cares ere greater sum arise. Read it sweet maid, though it be done but slightly; Who can show all his love, doth love but lightly."
    ],
    [
        "Write a poem like edmund spenser",
        "Ye tradefull Merchants that with weary toyle, Do seeke most pretious things to make your gain: And both the Indias of their treasures spoile, What needeth you to seeke so farre in vaine? For loe my love doth in her selfe containe All this worlds riches that may farre be found, If Saphyres, loe hir eies be Saphyres plaine, If Rubies, loe hir lips be Rubies sound: If Pearles, hir teeth be pearles both pure and round; If Yvorie, her forhead yvory weene; If Gold, her locks are finest gold on ground; If silver, her faire hands are silver sheene; But that which fairest is, but few behold, Her mind adornd with vertues manifold."
    ],
    [
        "Write a poem like louise bogan",
        "Louise Bogan, Cassandra from The Blue Estuaries: Poems 1923-1968. Copyright  1968 by Louise Bogan. Used by permission of Farrar, Straus & Giroux, LLC, http://us.macmillan.com/fsg. All rights reserved."
    ],
    [
        "Write a poem like marjorie pickthall",
        "Living, I had no might To make you hear, Now, in the inmost night, I am so near No whisper, falling light, Divides us, dear.  Living, I had no claim On your great hours. Now the thin candle-flame, The closing flowers, Wed summer with my name,  And these are ours.  Your shadow on the dust, Strength, and a cry, Delight, despair, mistrust,  All these am I. Dawn, and the far hills thrust To a far sky.  Living, I had no skill To stay your tread, Now all that was my will Silence has said. We are one for good and ill Since I am dead."
    ],
    [
        "Write a poem like michael anania",
        "Michael Anania, Waiting There from Selected Poems. Copyright  1994 by Michael Anania. Used by permission of Asphodel Press/Acorn Alliance."
    ],
    [
        "Write a poem like sir philip sidney",
        "Stella, since thou so right a princess art Of all the powers which life bestows on me, There ere by them aught undertaken be They first resort unto that sovereign part; Sweet, for a while give respite to my heart, Which pants as though it still should leap to thee, And on my thoughts give thy lieutenancy To this great cause, which needs both use and art, And as a queen, who from her presence sends Whom she employs, dismiss from thee my wit, Till it have wrought what thy own will attends. On servants shame oft masters blame doth sit. Oh let not fools in me thy works reprove, And scorning say, See what it is to love."
    ],
    [
        "Write a poem like william butler yeats",
        "I went out to the hazel wood, Because a fire was in my head, And cut and peeled a hazel wand, And hooked a berry to a thread; And when white moths were on the wing, And moth-like stars were flickering out, I dropped the berry in a stream And caught a little silver trout.  When I had laid it on the floor I went to blow the fire a-flame, But something rustled on the floor, And someone called me by my name: It had become a glimmering girl With apple blossom in her hair Who called me by my name and ran And faded through the brightening air.  Though I am old with wandering Through hollow lands and hilly lands, I will find out where she has gone, And kiss her lips and take her hands; And walk among long dappled grass, And pluck till time and times are done, The silver apples of the moon, The golden apples of the sun."
    ],
    [
        "Write a poem like sir walter ralegh",
        "Methought I saw the grave where Laura lay, Within that temple where the vestal flame Was wont to burn; and, passing by that way, To see that buried dust of living fame, Whose tomb fair Love, and fairer Virtue kept: All suddenly I saw the Fairy Queen; At whose approach the soul of Petrarch wept, And, from thenceforth, those Graces were not seen: For they this queen attended; in whose stead Oblivion laid him down on Lauras hearse: Hereat the hardest stones were seen to bleed, And groans of buried ghosts the heavens did pierce: Where Homers spright did tremble all for grief, And cursed the access of that celestial thief!"
    ],
    [
        "Write a poem like thomas campion",
        "Come, O come, my lifes delight, Let me not in languor pine! Love loves no delay; thy sight, The more enjoyed, the more divine: O come, and take from me The pain of being deprived of thee!  Thou all sweetness dost enclose, Like a little world of bliss. Beauty guards thy looks: the rose In them pure and eternal is. Come, then, and make thy flight As swift to me, as heavenly light."
    ],
    [
        "Write a poem like sir philip sidney",
        "Fly, fly, my friends, I have my death wound, fly! See there that boy, that murd'ring boy, I say, Who, like a thief, hid in dark bush doth lie Till bloody bullet get him wrongful prey. So tyrant he no fitter place could spy, Nor so fair level in so secret stay, As that sweet black which veils the heav'nly eye; There himself with his shot he close doth lay. Poor passenger, pass now thereby I did, And stay'd, pleas'd with the prospect of the place, While that black hue from me the bad guest hid; But straight I saw motions of lightning grace And then descried the glist'ring of his dart: But ere I could fly thence it pierc'd my heart."
    ],
    [
        "Write a poem like wallace stevens",
        "The trade-wind jingles the rings in the nets around the racks by the docks on Indian River. It is the same jingle of the water among roots under the banks of the palmettoes, It is the same jingle of the red-bird breasting the orange-treesout of the cedars. Yet there is no spring in Florida, neither in boskage perdu, nor on the nunnery beaches."
    ],
    [
        "Write a poem like sir walter ralegh",
        "As you came from the holy land Of Walsingham, Met you not with my true love By the way as you came?  How shall I know your true love, That have met many one, I went to the holy land, That have come, that have gone?  She is neither white, nor brown, But as the heavens fair; There is none hath a form so divine In the earth, or the air.  Such a one did I meet, good sir, Such an angelic face, Who like a queen, like a nymph, did appear By her gait, by her grace.  She hath left me here all alone, All alone, as unknown, Who sometimes did me lead with herself, And me loved as her own.  Whats the cause that she leaves you alone, And a new way doth take, Who loved you once as her own, And her joy did you make?  I have lovd her all my youth; But now old, as you see, Love likes not the falling fruit From the withered tree.  Know that Love is a careless child, And forgets promise past; He is blind, he is deaf when he list, And in faith never fast.  His desire is a dureless content, And a trustless joy: He is won with a world of despair, And is lost with a toy.  Of womenkind such indeed is the love, Or the word love abusd, Under which many childish desires And conceits are excusd.  But true love is a durable fire, In the mind ever burning, Never sick, never old, never dead, From itself never turning."
    ],
    [
        "Write a poem like samuel daniel",
        "When men shall find thy flower, thy glory pass, And thou, with careful brow sitting alone, Received hast this message from thy glass, That tells thee truth, and says that all is gone, Fresh shalt thou see in me the wounds thou madest, Though spent thy flame, in me the heat remaining, I that have loved thee thus before thou fadest, My faith shall wax, when thou art in thy waning. The world shall find this miracle in me, That fire can burn when all the matters spent; Then what my faith hath been thyself shall see, And that thou wast unkind thou mayst repent. Thou mayst repent that thou hast scorned my tears, When Winter snows upon thy golden hairs."
    ],
    [
        "Write a poem like d. h. lawrence",
        "My love looks like a girl to-night,       But she is old. The plaits that lie along her pillow       Are not gold, But threaded with filigree silver,       And uncanny cold.  She looks like a young maiden, since her brow       Is smooth and fair, Her cheeks are very smooth, her eyes are closed.       She sleeps a rare Still winsome sleep, so still, and so composed.  Nay, but she sleeps like a bride, and dreams her dreams       Of perfect things. She lies at last, the darling, in the shape of her dream,       And her dead mouth sings By its shape, like the thrushes in clear evenings."
    ],
    [
        "Write a poem like george gascoigne",
        "     Sing lullaby, as women do, Wherewith they bring their babes to rest, And lullaby can I sing too As womanly as can the best. With lullaby they still the child, And if I be not much beguiled, Full many wanton babes have I Which must be stilled with lullaby.       First lullaby my youthful years; It is now time to go to bed, For crooked age and hoary hairs Have won the haven within my head. With lullaby, then, youth be still; With lullaby content thy will; Since courage quails and comes behind, Go sleep, and so beguile thy mind.       Next, lullaby my gazing eyes, Which wonted were to glance apace. For every glass may now suffice To show the furrows in my face; With lullaby then wink awhile, With lullaby your looks beguile; Let no fair face nor beauty bright Entice you eft with vain delight.       And lullaby, my wanton will; Let reason's rule now reign thy thought, Since all too late I find by skill How dear I have thy fancies bought; With lullaby now take thine ease, With lullaby thy doubts appease. For trust to this: if thou be still, My body shall obey thy will.       Eke lullaby, my loving boy, My little Robin, take thy rest; Since age is cold and nothing coy, Keep close thy coin, for so is best; With lullaby be thou content, With lullaby thy lusts relent, Let others pay which hath mo pence; Thou art too poor for such expense.       Thus lullaby, my youth, mine eyes, My will, my ware, and all that was. I can no mo delays devise, But welcome pain, let pleasure pass; With lullaby now take your leave, With lullaby your dreams deceive; And when you rise with waking eye, Remember then this lullaby."
    ],
    [
        "Write a poem like william shakespeare",
        "From you have I been absent in the spring, When proud-pied April, dressed in all his trim, Hath put a spirit of youth in everything, That heavy Saturn laughed and leaped with him. Yet nor the lays of birds, nor the sweet smell Of different flowers in odour and in hue, Could make me any summers story tell, Or from their proud lap pluck them where they grew: Nor did I wonder at the lilys white, Nor praise the deep vermilion in the rose; They were but sweet, but figures of delight Drawn after you,  you pattern of all those.     Yet seemd it winter still, and, you away,     As with your shadow I with these did play."
    ],
    [
        "Write a poem like william shakespeare",
        "When to the sessions of sweet silent thought I summon up remembrance of things past, I sigh the lack of many a thing I sought, And with old woes new wail my dear time's waste: Then can I drown an eye, unus'd to flow, For precious friends hid in death's dateless night, And weep afresh love's long since cancell'd woe, And moan th' expense of many a vanish'd sight; Then can I grieve at grievances foregone, And heavily from woe to woe tell o'er The sad account of fore-bemoaned moan, Which I new pay as if not paid before. But if the while I think on thee, dear friend, All losses are restor'd, and sorrows end."
    ],
    [
        "Write a poem like sir philip sidney",
        "It is most true, that eyes are formed to serve The inward light; and that the heavenly part Ought to be king, from whose rules who do swerve, Rebels to Nature, strive for their own smart.     It is most true, what we call Cupids dart, An image is, which for ourselves we carve; And, fools, adore in temple of our heart, Till that good god make Church and churchman starve.     True, that true beauty virtue is indeed, Whereof this beauty can be but a shade, Which elements with mortal mixture breed; True, that on earth we are but pilgrims made,     And should in soul up to our country move; True; and yet true, that I must Stella love."
    ],
    [
        "Write a poem like william shakespeare",
        "Tir'd with all these, for restful death I cry, As, to behold desert a beggar born, And needy nothing trimm'd in jollity, And purest faith unhappily forsworn, And gilded honour shamefully misplac'd, And maiden virtue rudely strumpeted, And right perfection wrongfully disgrac'd, And strength by limping sway disabled, And art made tongue-tied by authority, And folly, doctor-like, controlling skill, And simple truth miscall'd simplicity, And captive good attending captain ill. Tir'd with all these, from these would I be gone, Save that, to die, I leave my love alone."
    ]
]


class OpenAi:

    def __init__(
        self,
        model,
        search_model,
        max_tokens
        ):
        # Model to use for the prediction
        self.model = model
        # Model to use for search
        self.search_model = search_model
        # Define a maximum number of tokens
        self.max_tokens = max_tokens

    def upload(self):
        return

    def completion(self):
        return

    # Question (required) - is the "prompt"
    # Exemples (required) - a list of key/value pair exemples to inspire the model
    # Exemples_context (required) - the probable output from the prompt
    # Documents (optional) needs to be a jsonl file or a dict/array
    def answers(self, question, examples, examples_context, documents,
                temperature, frequency_penalty, presence_penalty):
        response = openai.Answer.create(
            # search_model=self.search_model,
            model=self.model,
            question=question,
            max_tokens=self.max_tokens,
            examples=examples,
            examples_context=examples_context,
            documents=documents,
            temperature=temperature,
            frequency_penalty=frequency_penalty,
            presence_penalty=presence_penalty
        )
        return response

    # Generate Random Exemples/Documents from the dataset provided
    # Poorly reformated yet
    def get_random_documents(self):
        df = pd.read_csv('data/poems.csv')[['author', 'content']]
        df['author'] = df['author'].str.lower()
        df['content'] = df['content'].str.replace('\r\n', ' ')

        # Generate random documents
        _amount = 100

        # Generate random examples
        examples = []
        sample_df = df.sample(frac=1).reset_index(drop=True)[:_amount]
        for sample in sample_df.iterrows():
            # print(sample[1][1])
            if len(sample[1][1]) < 2048:
                examples.append(
                    [f'Write a poem like {sample[1][0]}', sample[1][1]])


        documents = []
        sample_df = df.sample(frac=1).reset_index(drop=True)[:_amount]
        for sample in sample_df.iterrows():
            if len(sample[1][1]) < 2048:
                documents.append(sample[1][1])

        return examples[:50], documents[:50]

    def get_random_documents_static(self):
        _rand = random.randint(0, 44)
        return EXAMPLES[_rand:_rand + 5], DOCUMENTS[_rand:_rand + 5]

    def predict_haiku(self,
                      question,
                      temperature=1,
                      frequency_penalty=-2.0,
                      presence_penalty=-2.0):
        examples_context = "you’re a beast, she said, your big white belly, and those hairy feet., you never cut your nails, and you have fat hands, paws like a cat, your bright red nose, and the biggest balls, I’ve ever seen, you shoot sperm like a, whale shoots water out of the, hole in its back, beast beast beast, she kissed me, what do you want for, breakfast?"
        examples, documents = self.get_random_documents_static()

        res = self.answers(
            question=question,
            examples=examples,
            examples_context=examples_context,
            documents=documents,
            temperature=temperature,
            frequency_penalty=frequency_penalty,
            presence_penalty=presence_penalty,
        )

        return res['answers']

    def predict_haiku_test(self, question, examples, examples_context, documents):
        res = self.answers(question=question,
                           examples=examples,
                           examples_context=examples_context,
                           documents=documents)
        return res

if __name__ == '__main__':
    # Initialise OpenAi with model and search model you desire
    # Be aware of the max number of tokens it returns
    gpt3 = OpenAi(
        model='davinci',
        search_model='curie',
        max_tokens=70
    )

    # print(gpt3.predict_haiku('Write a poem for my mom', temperature=0.9))

    exemples, documents = gpt3.get_random_documents_static()

    print(json.dumps(exemples, indent=2))
    print(json.dumps(documents, indent=2))












    # # Exemples for jokes
    # prompt_start = 'Write a poem like'
    # examples = [
    #     [
    #         f'{prompt_start} Muddy Waters',
    #         'I hear a lotta buzzing, sound like my little honey bee, I hear a lotta buzzing, sound like my little honey bee,   She been all around the world making honey, But now she is coming back home to me.'
    #     ],
    #     [
    #         f'{prompt_start} Roberto Bolano',
    #         'I dreamt of a difficult case, I saw corridors filled with cops, I saw interrogations left unresolved, The ignominious archives, And then I saw the detective, Return to the scene of the crime, Tranquil and alone.'
    #     ],
    #     [
    #         f'{prompt_start} Robert Frost',
    #         'Whose woods these are I think I know, His house is in the village though, He will not see me stopping here, To watch his woods fill up with snow.'
    #     ]
    # ]
    # examples_context = 'Whose woods these are I think I know, His house is in the village though, He will not see me stopping here, To watch his woods fill up with snow.'

    # documents = [
    #     "you’re a beast, she said, your big white belly, and those hairy feet., you never cut your nails, and you have fat hands, paws like a cat, your bright red nose, and the biggest balls, I’ve ever seen, you shoot sperm like a, whale shoots water out of the, hole in its back., beast beast beast,, she kissed me,, what do you want for, breakfast?"
    # ]

    # print(gpt3.predict_haiku('Write a poem about fish', examples, examples_context, documents))

    # # Clean DF
    # df = pd.read_csv('data/poems.csv')[['author', 'content']]
    # df['author'] = df['author'].str.lower()
    # df['content'] = df['content'].str.replace('\r\n', ' ')

    # _amount = 100
    # # Generate random examples
    # examples = []
    # sample_df = df.sample(frac=1).reset_index(drop=True)[:_amount]
    # for sample in sample_df.iterrows():
    #     # print(sample[1][1])
    #     if len(sample[1][1]) < 2048:
    #         examples.append(
    #             [f'Write a poem like {sample[1][0]}', sample[1][1]])

    # # Generate random context
    # fail = True
    # while fail:
    #     _examples_context = sample_df['content'][random.randint(0, _amount)]
    #     if len(sample_df['content'][random.randint(0, _amount)]) < 2048:
    #         examples_context = _examples_context
    #         fail = False

    # # Generate random documents
    # documents = []
    # sample_df = df.sample(frac=1).reset_index(drop=True)[:_amount]
    # for sample in sample_df.iterrows():
    #     if len(sample[1][1]) < 2048:
    #         documents.append(sample[1][1])

    # print(json.dumps(examples, indent=2))
    # print(examples_context)
    # print(json.dumps(documents, indent=2))

    # examples_context = 'Supper comes at five o\'clock, At six, the evening star, My lover comes at eight o\'clock, But eight o\'clock is far, How could I bear my pain all day, Unless I watched to see, The clock-hands laboring to bring Eight o\'clock to me.'

    # print(
    #     gpt3.predict_haiku_test('Write a poem about how today was a terrible', examples[:5], examples_context,
    #                     documents[:15]))

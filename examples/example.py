from robot_poetry.robot_poetry import RobotPoetry, Rhyming


print(Rhyming().words_that_rhyme_with('fun'), Rhyming.CLOSE_RHYMES)
print(Rhyming().does_it_rhyme('fun', 'begun'))
"""Output"""
# ['begun', 'bruhn', 'brun', 'brunn', 'bun', 'bunn', 'byun', etc]
# True

text = RobotPoetry('texts/hamlet.txt')
print(text.write_quad(2))

"""Output"""
# Or pour plausive but physic else forgone supply
# Dislike deserved quality, who any stated scratch keeps attribute
# Polonius, however thou understand both trust, army rely
# Yourself hide pastime on labour body sir pale methinks countersuit
#
# Forty its combination, armour stream, them sweet honesty
# Yourself 'twill do this proof tune
# Him you dispatch whereof dalgety
# Materials yet errors faith curse sleeping huntoon

text = RobotPoetry('texts/a_midsummer_night\'s_dream.txt')
print(text.write_quad(2))

"""Output"""
# Vile, queen white an estate
# Goblin whom know me hand
# Bottom fit those either beauties 30 extremely hoary-headed into straight
# Property thy pg serpent methinks put white asterisk wakes wieland
#
# Before wolf ravish us turn solemnly sheen half patent
# When rough devour conceits drew her conspir the moonbeams
# Idolatry jack, snow, thisby, pyramus conant
# Sword dost no found if either later midsummer wrong nordstroms
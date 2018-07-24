from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database import User,Categories, Base, Items

engine = create_engine('sqlite:///datamenu.db')
#engine = create_engine('postgresql://catalog:catalog@localhost/catalog')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)

session = DBSession()

#Create first user
User1 = User(name="Ankit Singh",email="mywish@.com")

session.add(User1)
session.commit()

cat = Categories(user_id=1, name="Soccor")

session.add(cat)
session.commit()

Litem1 = Items(user_id=1, name="Shinguards", description=" A shin guard or shin pad is a piece of equipment worn on the front of a players shin to protect them from injury. These are commonly used in sports including association football, baseball, ice hockey, field hockey, lacrosse, cricket, and other sports. This is due to either being required by the rules and laws of the sport or worn voluntarily by the participants for protective measures!!", categories=cat)

session.add(Litem1)
session.commit()


Litem1 = Items(user_id=1, name="Two shinguards", description="This technology dates back to ancient times as early as Greek and Roman Republics. Back then, shin guards were viewed as purely protective measures for warriors in battle and were made of bronze or other hard, sturdy materials. The earliest known physical proof of the technology appeared when archaeologist Sir William Temple discovered a pair of bronze greaves with a Gorgons head design in the relief on each knee capsule. After careful, proper examination it was estimated that the greaves were made in Apulia, a region in Southern Italy, around 550/500 B.C!!", categories=cat)

session.add(Litem1)
session.commit()

Litem1 = Items(user_id=1, name="Jersey", description="The bailiwick consists of the island of Jersey, the largest of the Channel Islands, along with surrounding uninhabited islands and rocks collectively named Les Dirouilles, Les Ecrehous, Les Minquiers, Les Pierres de Lecq, and other reefs. Although the bailiwicks of Jersey and Guernsey are often referred to collectively as the Channel Islands, the channel islands are not a constitutional or political unit. Jersey has a separate relationship to the Crown from the other Crown dependencies of Guernsey and the Isle of Man, although all are held by the monarch of the United Kingdom.",categories=cat)

session.add(Litem1)
session.commit()

Litem1 = Items(user_id=1, name="Soccor Cleats", description="Cleats or studs are protrusions on the sole of a shoe, or on an external attachment to a shoe, that provide additional traction on a soft or slippery surface. They can be conical or blade-like in shape, and made of plastic, rubber or metal. In American English the term cleats is used synecdochically to refer to shoes featuring such protrusions. Similarly, in British English the term 'studs' can be used to refer to 'football boots' or 'rugby boots', for instance, in a similar manner to the way 'spikes' is often used to refer to athletics shoes. The type of studs worn depends on the environment of play, whether it be grass, ice, artificial turf, or other grounds requiring versatility.",categories=cat)

session.add(Litem1)
session.commit()

cat = Categories(user_id=1, name="Frisbee")

session.add(cat)
session.commit()


Litem1 = Items(user_id=1, name="Frisbee", description="Flying discs are thrown and caught for free-form (freestyle) recreation and as part of many flying disc games. A wide range of flying disc variants are available commercially. Disc golf discs are usually smaller but denser and tailored for particular flight profiles to increase/decrease stability and distance.",categories=cat)

session.add(Litem1)
session.commit()

cat = Categories(user_id=1, name="Baseball")

session.add(cat)
session.commit()

Litem1 = Items(user_id=1, name="Bat", description="A baseball bat is a smooth wooden or metal club used in the sport of baseball to hit the ball after it is thrown by the pitcher. By regulation it may be no more than 2.75 inches (70 mm) in diameter at the thickest part and no more than 42 inches (1,100 mm) long. Although historically bats approaching 3 pounds (1.4 kg) were swung, today bats of 33 ounces (0.94 kg) are common, topping out at 34 ounces (0.96 kg) to 36 ounces (1.0 kg).",categories=cat)

session.add(Litem1)
session.commit()

cat = Categories(user_id=1, name="Hockey")

session.add(cat)
session.commit()


Litem1 = Items(user_id=1, name="Stick", description="A hockey stick is a piece of equipment used by the players in most forms of hockey to move the ball or puck. Different variations throughout history have been utilised for various sports. The common shape includes a long staff with a curved flattened end. The end and curvature of the stick is normally the variant between different sports.",categories=cat)

session.add(Litem1)
session.commit()
cat = Categories(user_id=1, name="Snowboarding")

session.add(cat)
session.commit()


Litem1 = Items(user_id=1, name="Goggles", description="Goggles, or safety glasses, are forms of protective eyewear that usually enclose or protect the area surrounding the eye in order to prevent particulates, water or chemicals from striking the eyes. They are used in chemistry laboratories and in woodworking. They are often used in snow sports as well, and in swimming. Goggles are often worn when using power tools such as drills or chainsaws to prevent flying particles from damaging the eyes. Many types of goggles are available as prescription goggles for those with vision problems.",categories=cat)

session.add(Litem1)
session.commit()


Litem1 = Items(user_id=1, name="Snowboard", description="Snowboards are boards where both feet are secured to the same board, which are wider than skis, with the ability to glide on snow.Snowboards widths are between 6 and 12 inches or 15 to 30 centimeters.Snowboards are differentiated from monoskis by the stance of the user. In monoskiing, the user stands with feet inline with direction of travel (facing tip of monoski/downhill) (parallel to long axis of board), whereas in snowboarding, users stand with feet transverse (more or less) to the longitude of the board. Users of such equipment may be referred to as snowboarders.",categories=cat)

session.add(Litem1)
session.commit()

print "Litem added"

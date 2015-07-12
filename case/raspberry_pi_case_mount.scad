$fn=30;
height=80;
module pir_holder(){
   lense_cover=23.35;
	hole_offset=3.25;
	hole_size=2.2;
	flange=5;
	union(){
		square([lense_cover, lense_cover], center=true);
		//#square([lense_cover+flange*2, lense_cover], center=true);
		translate([lense_cover/2+hole_offset,0]) circle(d=hole_size);
		translate([-(lense_cover/2+hole_offset),0]) circle(d=hole_size);
	}
}
module mounting_plate(){
	case_inner_width=58.5;
	square([case_inner_width, height], center=true);
}
difference(){
	mounting_plate();
	translate([0, height/2 - 15]) pir_holder();
}

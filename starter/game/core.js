export const WIDTH=640, HEIGHT=400;
export function initialState() {
  return {player:{x:320,y:200,r:10},enemy:{x:50,y:50,r:12},elapsed:0,over:false};
}
export function update(s, input, dt) {
  if(s.over) return;
  const seconds=Math.min(Math.max(Number.isFinite(dt)?dt:0,0),0.05);
  let x=Number(input.right)-Number(input.left), y=Number(input.down)-Number(input.up);
  const length=Math.hypot(x,y)||1;
  s.player.x=Math.max(10,Math.min(WIDTH-10,s.player.x+x/length*180*seconds));
  s.player.y=Math.max(10,Math.min(HEIGHT-10,s.player.y+y/length*180*seconds));
  const dx=s.player.x-s.enemy.x,dy=s.player.y-s.enemy.y,d=Math.hypot(dx,dy)||1;
  s.enemy.x+=dx/d*75*seconds; s.enemy.y+=dy/d*75*seconds;
  s.elapsed+=seconds;
  if(Math.hypot(s.player.x-s.enemy.x,s.player.y-s.enemy.y)<=s.player.r+s.enemy.r) s.over=true;
}

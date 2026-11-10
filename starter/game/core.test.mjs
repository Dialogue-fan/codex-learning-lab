import test from 'node:test';
import assert from 'node:assert/strict';
import {initialState,update} from './core.js';
const none={left:false,right:false,up:false,down:false};
test('运动按时间计算，对角线不加速',()=>{const a=initialState(),b=initialState();update(a,{...none,right:true},.01);update(b,{...none,right:true,down:true},.01);assert.ok(Math.abs(Math.hypot(a.player.x-320,a.player.y-200)-Math.hypot(b.player.x-320,b.player.y-200))<1e-8);});
test('边界限制，碰撞结束后停止更新',()=>{const s=initialState();s.player.x=630;update(s,{...none,right:true},.05);assert.equal(s.player.x,630);s.enemy={...s.player};update(s,none,.01);assert.equal(s.over,true);const old=structuredClone(s);update(s,{...none,left:true},.05);assert.deepEqual(s,old);});
test('重开得到独立初始状态；异常长帧被限制',()=>{const a=initialState();update(a,none,50);assert.equal(a.elapsed,.05);a.over=true;const b=initialState();assert.equal(b.over,false);assert.equal(b.elapsed,0);assert.notEqual(a.player,b.player);});

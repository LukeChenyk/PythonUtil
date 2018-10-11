package com.game.user.quickbattle.packet;

/**
 * lilili
 */
public class SM_PlayerInfo {

    /** id */
    public int id;

    /** 名字 */
    public String name;//测试

    /**
     * 年龄
     */
    public int age;

    /** 钱 */
    private long _money;

    /** 布尔 */
    private boolean isAuto;

    private Map<Integer, Integer> aSimpleMap;

    /** a list */
    private List<LevelChangeAndExp> aSimpleList;

    //测试吧

    public int sum(){
        return 0;
    }

}
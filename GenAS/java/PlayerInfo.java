package com.game.user.quickbattle.packet;

import java.util.List;
import java.util.List;

/**
 * lilili
 */
public class PlayerInfo {

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

    /** a list */
    private List<Integer> intList;

    private LevelChangeAndExp oneBean;

    private byte oneByte;

    //测试吧

    public int sum(){
        return 0;
    }

}
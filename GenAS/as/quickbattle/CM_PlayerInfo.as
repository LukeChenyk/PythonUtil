package com.protocol.quickbattle {

	import com.common.connect.structure.Message;
	import com.common.connect.utils.long;
	import com.protocol.MapType;

	/**
	 * AutoGen
	 */
	public class CM_PlayerInfo  extends Message {
	
	    /** id */
	    public var id:int;
	
	    /** 名字 */
	    public var name:String;//测试
	
	    /**
	     * 年龄
	     */
	    public var age:int;
	
	    /** 钱 */
	    public var money:long;
	
	    /** 布尔 */
	    public var isAuto:Boolean;
	
	    public var aSimpleMap:Object;
	
	    /** a list */
	    public var aSimpleList:Vector.<LevelChangeAndExp>;
	
	    /** a list */
	    public var intList:Vector.<int>;
	
	    public var oneBean:LevelChangeAndExp;
	
	    public var oneByte:int;

		override protected function writing():Boolean {
			id = writeInt();
			name = writeString();
			age = writeInt();
			money = writeLong();
			isAuto = writeBoolean();
			aSimpleMap = writeObject(MapType.INT, MapType.INT, null, null);
			aSimpleList = writeArray(MapType.BEAN, LevelChangeAndExp);
			intList = writeArray(MapType.INT, null);
			oneBean = writeBean(LevelChangeAndExp);
			oneByte = writeByte();
			return true;
		}

	}
}

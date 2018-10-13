package com.protocol.quickbattle {

	import com.common.connect.structure.Message;
	import com.common.connect.utils.long;
	import com.protocol.MapType;

	/**
	 * AutoGen
	 */
	public class SM_PlayerInfo  extends Message {
	
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

		override protected function reading():Boolean {
			id = readInt();
			name = readString();
			age = readInt();
			money = readLong();
			isAuto = readBoolean();
			aSimpleMap = readObject(MapType.INT, MapType.INT, null, null);
			aSimpleList = readArray(MapType.BEAN, LevelChangeAndExp);
			intList = readArray(MapType.INT, null);
			oneBean = readBean(LevelChangeAndExp);
			oneByte = readByte();
			return true;
		}

		override public function getId():int {
			return -xxxx;
		}

	}
}

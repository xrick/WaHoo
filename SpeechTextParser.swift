//
//  SpeechTextParser.swift
//  MyVoiceIdentifier
//
//  Created by justin on 2018/10/25.
//  Copyright © 2018年 tw.com.habook. All rights reserved.
//

import Foundation

public class SpeechTextParser {
    public static let speechLangZh:Int = 1;
    
    private var speechLang = 0
    private var commandFilter: CommandFilter?
    
    public init(speechLang: Int) {
        self.speechLang = speechLang
        
        if SpeechTextParser.speechLangZh == speechLang {
            self.commandFilter = ZhCommandFilter()
        }
    }
    
    public func parse(rawText: String) -> SpeechCommand? {
        guard let commandFilter = self.commandFilter else {
            return nil
        }
        
        //切詞
        SegmentorWrapper().jiebaInit()
        let cutStringArray = SegmentorWrapper().jiebaCut(for: rawText) as! [String]
        
        //過濾多個指令，只留最後一組
        let commandStringArray:[String]? = commandFilter.filterPrefix(segArr: cutStringArray)
        if commandStringArray == nil {
            return nil
        }
        print("\(String(describing: commandStringArray))")
        
        //取得指令
        //  - 先以 常規式 檢查是否有指令
        //  - 再以 正面表列關鍵字 比對是否有指令
        var action:String? = commandFilter.filterActionReg(segArr: commandStringArray)
        var paramStringArray = [String]()
        if action != nil {
            paramStringArray = commandStringArray!
        } else {
            let actionIndex:Int? = commandFilter.filterActionIndex(segArr: commandStringArray)
            if actionIndex==nil || actionIndex == SpeechCommand.actionIndexNotFound {
                return nil
            } else if actionIndex! >= commandStringArray?.count ?? SpeechCommand.actionIndexNotFound {
                return nil
            }
            
            let seg = commandStringArray?[actionIndex!]
            var segNext = seg
            if actionIndex != commandStringArray!.count-1 {
                segNext = commandStringArray![actionIndex!+1]
            }
            action = commandFilter.convertActionFirstStage(actionText: seg, actionTextNext: segNext)
            if action == nil {
                action = commandFilter.convertActionSecondStage(actionText: commandStringArray?[actionIndex!])
            }
            
            //取得處理參數用的 stringArray - 將 commandStringArray 從 actionIndex 之後的元素取出
            if commandStringArray!.count-(actionIndex!+1) > 0 {
                for index in actionIndex!+1...commandStringArray!.count-1 {
                    paramStringArray.append((commandStringArray?[index])!)
                }
            }
        }
        if action == nil {
            return nil
        }
        
        //依指令判斷是否要處理參數及參數修飾
        var param: Int! = SpeechCommand.ParamConstant.paramUndefined
        var paramDecoration: Int! = SpeechCommand.ParamDecorationConstant.paramDecorationUndefined
        if action == SpeechCommand.ActionTypeConstant.actionTypePick {
            var temp = commandFilter.filterPickParam(segArr: paramStringArray)
            if temp != SpeechCommand.ParamConstant.paramUndefined {
                param = temp
                
                temp = self.commandFilter?.filterPickParamDecoration(segArr: paramStringArray)
                if temp != SpeechCommand.ParamDecorationConstant.paramDecorationUndefined {
                    paramDecoration = temp
                }
            } else {
                return nil //挑人 必須有人數
            }
        } else if action == SpeechCommand.ActionTypeConstant.actionTypeStatic {
            let temp = commandFilter.filterStaticParam(segArr: paramStringArray)
            if temp != SpeechCommand.ParamConstant.paramUndefined {
                param = temp
            } else {
                return nil //統計與排行 必須有圖表類型
            }
        } else if action == SpeechCommand.ActionTypeConstant.actionTypeCountDown {
            let temp = commandFilter.filterCountDownParam(segArr: paramStringArray)
            if temp != SpeechCommand.ParamConstant.paramUndefined {
                param = temp
            } else {
                return nil //計時器 必須有秒數
            }
        } else if action == SpeechCommand.ActionTypeConstant.actionTypeScore {
            var temp = commandFilter.filterScoreParam(segArr: paramStringArray)
            if temp != SpeechCommand.ParamConstant.paramUndefined {
                param = temp
                
                temp = commandFilter.filterScoreParamDecoration(segArr: paramStringArray)
                if temp != SpeechCommand.ParamDecorationConstant.paramDecorationUndefined {
                    paramDecoration = temp
                }
            } else {
                return nil //計分板 必須有分數
            }
        }
        
        //產出回傳物件
        let speechCommand = SpeechCommand()
        speechCommand.rawText = rawText
        speechCommand.action = action
        speechCommand.param = param
        speechCommand.paramDecoration = paramDecoration
        return speechCommand
    }
}

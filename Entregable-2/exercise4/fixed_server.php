<?php

class LangMgr
{
    public function newLang()
    {
        $lang = $this->getBrowserLang();
        $sanitizedLang = $this->sanitizeLang($lang);
        require_once "/lang/$sanitizedLang";
    }

    private function getBrowserLang()
    {
        $lang = $_SERVER['HTTP_ACCEPT_LANGUAGE'] ?? 'en';
        return $lang;
    }

    private function sanitizeLang($lang)
    {
        $path = "/lang/$lang";
        if($path === realpath($path)) return $lang;
        return 'en';
    }
}

(new LangMgr())->newLang();

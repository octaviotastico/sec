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
        return str_replace('../', '', $lang);
    }
}

(new LangMgr())->newLang();
